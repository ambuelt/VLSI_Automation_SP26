################################################################################
# Clean Static Timing Analysis Program
# Simplified version of original project code
################################################################################

import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict, deque


################################################################################
# Node Class (Represents a gate in the circuit)
################################################################################

class Node:
    def __init__(self, name, gate_type):

        self.name = name
        self.gate_type = gate_type

        # Connectivity
        self.fanin = []
        self.fanout = []

        # Load capacitance
        self.Cload = 0.0

        # Timing values
        self.Tau_out = 0.0
        self.max_out_arrival = 0.0
        self.required_time = float("inf")
        self.slack = 0.0

        # Store delay from each input
        self.cell_delays = {}



################################################################################
# LUT Class (Stores NLDM library)
################################################################################

class LUT:

    def __init__(self):
        self.full_cell = {}

    ###########################################################################
    # Parse NLDM Library
    ###########################################################################
    def parse_nldm(self, file):

        with open(file) as f:
            text = f.read()

        cells = re.findall(r"cell\s*\(\s*(.*?)\)\s*\{(.*?)\}", text, re.S)

        for cell_name, body in cells:

            cap = float(re.findall(r'capacitance\s*:\s*([\d\.]+)', body)[0])

            index1 = re.findall(r'index_1\s*\("(.*?)"\)', body)[0]
            index2 = re.findall(r'index_2\s*\("(.*?)"\)', body)[0]

            tau_vals = np.array([float(x) for x in index1.split(",")])
            cap_vals = np.array([float(x) for x in index2.split(",")])

            values = re.findall(r'values\s*\((.*?)\);', body, re.S)

            delay_rows = re.findall(r'"(.*?)"', values[0])
            slew_rows = re.findall(r'"(.*?)"', values[1])

            delay = np.array([[float(x) for x in r.split(",")] for r in delay_rows])
            slew = np.array([[float(x) for x in r.split(",")] for r in slew_rows])

            self.full_cell[cell_name] = {
                "input_cap": cap,
                "index_1": tau_vals,
                "index_2": cap_vals,
                "delays": delay,
                "slews": slew
            }



################################################################################
# Helper: Gate Name Mapping
################################################################################

GATE_MAP = {
    "BUFF": "BUF_X1",
    "NOT": "INV_X1"
}

def get_gate_name(gtype):
    return GATE_MAP.get(gtype, f"{gtype}2_X1")



################################################################################
# Bilinear Interpolation
################################################################################

def interpolate(slew, cap, xvals, yvals, table):

    x = np.searchsorted(xvals, slew) - 1
    y = np.searchsorted(yvals, cap) - 1

    x = max(0, min(x, len(xvals)-2))
    y = max(0, min(y, len(yvals)-2))

    x1, x2 = xvals[x], xvals[x+1]
    y1, y2 = yvals[y], yvals[y+1]

    v11 = table[x][y]
    v12 = table[x][y+1]
    v21 = table[x+1][y]
    v22 = table[x+1][y+1]

    return (
        v11*(x2-slew)*(y2-cap) +
        v12*(x2-slew)*(cap-y1) +
        v21*(slew-x1)*(y2-cap) +
        v22*(slew-x1)*(cap-y1)
    ) / ((x2-x1)*(y2-y1))



################################################################################
# Topological Sort
################################################################################

def topological_sort(nodes):

    indegree = {n: len(n.fanin) for n in nodes}
    queue = deque([n for n in nodes if indegree[n] == 0])

    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for f in node.fanout:
            indegree[f] -= 1
            if indegree[f] == 0:
                queue.append(f)

    return order



################################################################################
# Compute Load Capacitance
################################################################################

def compute_cload(nodes, lut):

    for node in nodes:

        if node.gate_type in ["INPUT","OUTPUT"]:
            continue

        total = 0

        for fo in node.fanout:

            if fo.gate_type == "OUTPUT":
                total += 4 * lut.full_cell["INV_X1"]["input_cap"]

            else:
                gname = get_gate_name(fo.gate_type)
                total += lut.full_cell[gname]["input_cap"]

        node.Cload = total



################################################################################
# Forward Static Timing Analysis
################################################################################

def forward_sta(nodes, lut):

    order = topological_sort(nodes)

    for node in order:

        if node.gate_type == "INPUT":
            continue

        if node.gate_type == "OUTPUT":
            prev = node.fanin[0]
            node.max_out_arrival = prev.max_out_arrival
            continue

        gname = get_gate_name(node.gate_type)
        cell = lut.full_cell[gname]

        best_arrival = 0
        best_slew = 0

        for fin in node.fanin:

            tau = fin.Tau_out
            a_in = fin.max_out_arrival

            delay = interpolate(
                tau, node.Cload,
                cell["index_1"],
                cell["index_2"],
                cell["delays"]
            )

            slew = interpolate(
                tau, node.Cload,
                cell["index_1"],
                cell["index_2"],
                cell["slews"]
            )

            a_out = a_in + delay
            node.cell_delays[fin] = delay

            if a_out > best_arrival:
                best_arrival = a_out
                best_slew = slew

        node.max_out_arrival = best_arrival
        node.Tau_out = best_slew



################################################################################
# Backward Static Timing Analysis
################################################################################

def backward_sta(nodes, delay):

    required = 1.1 * delay

    order = topological_sort(nodes)[::-1]

    for node in order:

        if node.gate_type == "OUTPUT":
            node.required_time = required

        for fin in node.fanin:

            d = node.cell_delays.get(fin, 0)
            fin.required_time = min(fin.required_time,
                                    node.required_time - d)

    for n in nodes:
        n.slack = n.required_time - n.max_out_arrival



################################################################################
# Parse BENCH Circuit
################################################################################

def parse_bench(file, lut=None):

    nodes = {}
    wires = {}

    with open(file) as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line.startswith("INPUT"):

                w = re.findall(r'\((.*?)\)', line)[0]
                node = Node(f"INPUT-{w}", "INPUT")

                node.Tau_out = 0.002
                nodes[node.name] = node
                wires[w] = node

            elif line.startswith("OUTPUT"):

                w = re.findall(r'\((.*?)\)', line)[0]
                node = Node(f"OUTPUT-{w}", "OUTPUT")

                nodes[node.name] = node
                wires[w] = node

            else:

                out, expr = line.split("=")
                gtype = re.findall(r'(\w+)\(', expr)[0]
                ins = re.findall(r'\((.*?)\)', expr)[0].split(",")

                node = Node(f"{gtype}-{out.strip()}", gtype)

                nodes[node.name] = node
                wires[out.strip()] = node

                for w in ins:
                    if w in wires:
                        node.fanin.append(wires[w])
                        wires[w].fanout.append(node)

    node_list = list(nodes.values())

    if lut:

        compute_cload(node_list, lut)
        forward_sta(node_list, lut)

        delay = max(n.max_out_arrival for n in node_list
                    if n.gate_type == "OUTPUT")

        backward_sta(node_list, delay)

        print(f"Circuit Delay: {delay*1000:.4f} ps")



################################################################################
# Main
################################################################################

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--read_ckt", type=pathlib.Path)
    parser.add_argument("--read_nldm", type=pathlib.Path)

    args = parser.parse_args()

    lut = None

    if args.read_nldm:
        lut = LUT()
        lut.parse_nldm(args.read_nldm)

    if args.read_ckt:
        parse_bench(args.read_ckt, lut)
