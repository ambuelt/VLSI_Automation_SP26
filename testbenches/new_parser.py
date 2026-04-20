################################################################################
# Assignment : Mini-Project 1                                                  #
# Team: Ctrl Freaks                                                            #
# ---------------------------------------------------------------------------  #
#                                                                              #
# Parser File to Read circuits using Node class and NLDM library files         #
# using LUT class to generate the netlist and get gate info into txt files     #
# to traverse the circuit and calculate delays and critical path.              #
################################################################################

# All automatically in python 3.7 terminal except for numpy and pathlib
import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict
from collections import deque

import LUT as LUT
import Node as Node

def connect_inputs(gate_connections, nodes: dict):
    """
    Connects the primary inputs and mid-level gate inputs in the circuit
    
    :param input_wires: Represents the inputs to a node/vertice
    :param nodes: Represnts the Node object
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """

    ckt_wires = {}  # Stores all the wires for connections using there identifier number as the key to store nodes to connect
                    # Ex. '1' : INPUT-1 Node Object {all node details}

    # Iterates through all created nodes and splits the names by using [-1] to grab the last item in the list from the split
    for n in nodes.values():
        if (n.gate_type == "OUTPUT"):
            continue
        
        wire = n.name.split('-', 1)[-1]
        ckt_wires[wire] = n

    # Checks all inputs for that node against the node values to determine where they are in circuit
    # Used COdex to fix this function since I originally had it running when gate_type nodes that weren't INPUTs or OUTPUTs were created,
    # but this gave an issue when there were input gates into other gates that hadn't been created yet so gate_connections was made as a solution
    # Uses gate_connections list of tuples of all connections to a specific gate that was updated all through parsing
    # gate_n = gate_names, output wires, and input wires are all values in each tuple
    for gate_n, output_w, input_w in gate_connections:

        gate_node = nodes[gate_n]  # Identifies the current node to create the fanin for using the names in the gate_connections

        # Check all inputs of a gate to create the fanin network for that gate and fanout for input_gate
        for w in input_w:
            input = w.strip()
            input_node = ckt_wires[input]

            # Add all fanin and fanouts to circuit
            gate_node.fanin.append(input_node)   # Input -> Node
            input_node.fanout.append(gate_node)  # Input <- Node

            # Used to check the updated node objects
            #print(f'\nafter connected input node name {vars(gate_node)}\n')
            #print(f'\nafter connected input node name {vars(input_node)}\n')


def connect_outputs(output_wires, nodes: dict):
    """
    Connects final outputs of the circuit
    
    :param output_wires: Represents the outputs of a node/vertice
    :param nodes: Represnts the object node
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """

    ckt_wires = {}  # Stores all the wires for connections using there identifier number as the key to store nodes to connect
                    # Ex. '1' : INPUT-1 Node Object {all node details}

    for n in nodes.values():
        if (n.gate_type != "OUTPUT"):
            wire = n.name.split('-', 1)[-1]
            ckt_wires[wire] = n

    
    # Checks all output_wires against the node values to determine where they are in circuit
    for output in output_wires:

        output_name = f'OUTPUT-{output}'   # Name of primary output
        output_node = nodes[output_name]   # Check for primary output object
        last_node = ckt_wires[output]
  
        # Add all fanin and fanouts to circuit - need to use node.name otherwise it will add the Node object and not a string (made issues in printing)
        last_node.fanout.append(output_node) # Node -> Output
        output_node.fanin.append(last_node)  # Node <- Output

        # Used to check the updated node objects
        #print(f'\nafter connected output node name {vars(node)}\n')
        #print(f'\nafter connected output node name {vars(output_node)}\n')


# Officially works!!!!!!!
def write_ckt_output(ckt_inputs, ckt_outputs, gate_counter, nodes, output_file='ckt_details.txt'):
    """
    Prints the netlist file as described in appendix 1
    
    :param ckt_inputs: Tracks the a number of primary inputs created (list contains indentfying number for those inputs)
    :param ckt_outputs: Tracks the a number of primary outputs created (list contains indentfying number for those outputs)
    :param gate_counter: A defaultdict that tracks the total number of gates of each type
    :param nodes: A dict that contains all node objects
    :param output_file: Gives the name of the .txt to write to
    """

    # Open output circuit file for writing line by line
    with open(output_file, 'w') as ckt_file:
        ckt_file.write(f'{len(ckt_inputs)} primary inputs\n')
        ckt_file.write(f'{len(ckt_outputs)} primary outputs\n')

        # Iterate through gate types to print all gate values per type
        for gate_type, count in gate_counter.items():
            ckt_file.write(f'{count} {gate_type} gates\n')

        # Fanout of specific gates
        ckt_file.write('\nFanout...\n')
        
        # Iterate through all node values
        for node in nodes.values():
            if not ((node.gate_type == 'INPUT') or (node.gate_type == 'OUTPUT')):   # Don't want to print these due to the assignment formatting
                
                fanout_values = []  # Will store all the gate_names for the fanout of that node

                # Iterate through all fanout values and store the names of those nodes
                for n in node.fanout:
                    fanout_values.append(n.name)

                # Write all fanout node pairs and use .join concatinate all output node names
                ckt_file.write(f'{node.name}: ' + ', '.join(fanout_values) + '\n')


        # Fanin of specific gates
        ckt_file.write('\nFanin...\n')

        # Iterate through all node values
        for node in nodes.values():
            if not ((node.gate_type == 'INPUT') or (node.gate_type == 'OUTPUT')):  # Don't want to print these due to the assignment formatting
                
                fanin_values = []  # Will store all the gate_names for the fanin of that node

                # Iterate through all fanout values and store the names of those nodes
                for n in node.fanin:
                    fanin_values.append(n.name)

                # Write all fanout node pairs and use .join concatinate all input node names
                ckt_file.write(f'{node.name}: ' + ', '.join(fanin_values) + '\n')


def format_num_outputs(value):
    return f'{value * 1000:.6g}'



def write_ckt_traversal(ckt_delay, nodes, path, output_file='ckt_traversal.txt'):
    """
    Prints the output of traversal calculations as described in appendix 2
    
    :param ckt_delay: Stores the delay from start to finish of the circuit
    :param nodes: A dict that contains all node objects
    :param path: A list of all the names of the gates in the critical path
    :param output_file: Gives the name of the .txt to write to
    """

    # Open output circuit file for writing line by line
    with open(output_file, 'w') as ckt_file:
        ckt_file.write(f'Circuit delay: {format_num_outputs(ckt_delay)} ps\n')     # Multiply by 1000 for formatting

        # Fanout of specific gates
        ckt_file.write('\nGate slacks:\n')

        # Iterate through all node values and Write all node names and output slack at each node
        for node in nodes.values():
            ckt_file.write(f'{node.name}: {format_num_outputs(node.slack)} ps\n')  # Multiply by 1000 for formatting

        ckt_file.write(f'\nCritical path:\n')
        ckt_file.write(f','.join(path))



def compute_cload(nodes, lut):
    """
    Computes all the Cloads for each node by using the fanout of that gate and grabbing all the input caps of those gates 
    and adding them together

    :param nodes: A dict that contains all node objects
    :param lut: LUT object to be used for getting values from parsing nldm
    """

    # Iterate through all node values
    for node in nodes.values():
        total_cap = 0.0  # Stores the total added Cins from all fanout nodes for the current node

        # There should be no need to compute Cload for INPUTS and OUTPUTs since they have the Cin/Cload from the gates they are connected to
        if node.gate_type in ['INPUT', 'OUTPUT']:
            continue

        # Check all the connected fanout gates of the current node
        for fan_o in node.fanout:

            # Based on assignment instructions OUTPUT CLoad = 4 * inv_Cin
            if fan_o.gate_type == 'OUTPUT':
                total_cap += 4 * lut.full_cell['INV_X1']['input_cap']
            
            # If the gate_type is a regular logic gate
            else:
                
                # Make Sure that the names from the current nodes are edited so they can be used to determine which cell from the nldm is needed as the key for the dict
                if fan_o.gate_type == 'BUFF':
                    gate_name = 'BUF_X1'
                elif fan_o.gate_type == 'NOT':
                    gate_name = 'INV_X1'
                else:
                    gate_name = fan_o.gate_type + '2_X1'

                # Keep adding to the total capacitance for each fanout logic gate
                total_cap += lut.full_cell[gate_name]['input_cap']

        # Once all Cins of fanout gates have been added together for the current node, set it to be the Cload
        node.Cload = total_cap


def interpolate_arrays(slew_row, cap_col, xvals, yvals, array_2d_vals):
    """
    Follows the steps from appendix 3 for when the actual input slew and load cap doesn't match a specific delay

    :param slew_row: Actual input slew value
    :param cap_col: Actual load capacitance value
    :param xvals: index_1 array
    :param yvals: index_1 array
    :param array_2d_vals: 7x7 array of cell_delay or output_slew

    return interpolated_value : will give interpolated v value as listed in appendix 3
    """
    # Since the list of input slews and load caps are sorted, can search the list for the positions
    # Since slew_row is the actual input slew and between two values, need to find the bounds it falls between
    # To find the lower bound using -1
    x = np.searchsorted(xvals, slew_row) - 1
    y = np.searchsorted(yvals, cap_col)  - 1

    # Was having bounds issues and Codex gave the following two lines as a solution
    # -2 makes it so that x+1 and y+1 are valid
    x = max(0, min(x, len(xvals)-2))
    y = max(0, min(y, len(yvals)-2))

    # Get the two rows and two column values to used in the equation for value v
    slew1, slew2   = xvals[x], xvals[x+1]
    cap1, cap2     = yvals[y], yvals[y+1]

    # Determine the square values to check to compute interpolated value like in appendix 3, Figure 3
    v11 = array_2d_vals[x][y]
    v12 = array_2d_vals[x][y+1]
    v21 = array_2d_vals[x+1][y]
    v22 = array_2d_vals[x+1][y+1]

    # Appendix 3 equation where cap_col is C and slew_row is Tau
    numerator = (v11 * (cap2 - cap_col)*(slew2 - slew_row)) + (v12 * (cap_col - cap1)*(slew2 - slew_row)) + (v21 * (cap2 - cap_col)*(slew_row - slew1)) + (v22 * (cap_col - cap1)*(slew_row - slew1))
    denominator = (cap2 - cap1) * (slew2 - slew1)

    # Calulate the final interpoloated value using the equation from appendix 3
    interpolated_value = numerator / denominator
    return interpolated_value


def topological_order(nodes):
    """
    Computes the tpological sorting of all the logic gates in the circuit to be used for forward and backward traversal

    Used geeksforgeeks as baseline for topological sort (https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/)

    :param nodes: A dict that contains all node objects

    return gate_order : will make sure that the gates are listed from START -> END
    """
    gate_order = []   # Used to store all the node objects and return their final gate_order
    indegree = {}     # Calculates the number of unvisited nodes pointing to the current node
    queue = deque()   # queue is used to push/pop nodes to determine if they have been visited

    # Compute indegrees for each node
    for node in nodes.values():
        indegree[node.name] = len(node.fanin)   # Track the number of nodes pointing to the current node via the fanin

        # Currently will just store all INPUT nodes since they should not have anything pointing to them
        if indegree[node.name] == 0:
            queue.append(node)

    # Kahn’s BFS Algorithm
    while queue:
        node = queue.popleft()       # Pop the first node on the queue
        gate_order.append(node)      # Add node to visited nodes in the gate order

        # Check all connected nodes via the fanout
        for next_node in node.fanout:
            indegree[next_node.name] -= 1 # Subtract the indegree of next_node since others were processed

            # If next_node is connected to previous node
            if indegree[next_node.name] == 0:
                queue.append(next_node)

    return gate_order


def forward_sta(nodes, lut, order):
    """
    Moves forward through the circuit START -> END to calculate the delay and mex_out_arrival time of each node

    :param nodes: A dict that contains all node objects
    :param lut: LUT object to be used for getting values from parsing nldm
    """

    # Iterate through gates from INPUTs to OUTPUTs in the circuit
    for gate in order:
        node = nodes[gate.name]

        # Since INPUT values were already determined when they were initilalized, can skip them
        if node.gate_type == 'INPUT':
            continue

        # Make sure that max_out_arrival of OUTPUT nodes is set to be equal to the gate it is connected to since OUTPUT nodes don't have delay
        if node.gate_type == 'OUTPUT':
            prev_node = node.fanin[0]  # Identifies sole fanin for output
            node.max_out_arrival = prev_node.max_out_arrival

            node.inp_arrival.append(node.max_out_arrival)
            node.outp_arrival.append(node.max_out_arrival)
            continue

        max_arrival_time, fastest_slew = 0.0, 0.0  # Used to track the max a_out and best input slew for the gate

        # Make Sure that the names from the current nodes are edited so they can be used to determine which cell from the nldm is needed as the key for the dict
        if node.gate_type == 'BUFF':
                gate_name = 'BUF_X1'
        elif node.gate_type == 'NOT':
            gate_name = 'INV_X1'
        else:
            gate_name = node.gate_type + '2_X1'

        # Grab values from the LUT object
        slew_array = lut.full_cell[gate_name]['index_1']
        cap_array = lut.full_cell[gate_name]['index_2']
        gate_delay_array = lut.full_cell[gate_name]['delays']
        gate_slew_array = lut.full_cell[gate_name]['slews']

        num_inputs = len(node.fanin)  # Computes the number of gates input into the current node

        # Iterate through all fanin for the current node
        for fan_in in node.fanin:
            prev_node = nodes[fan_in.name]

            # Calculate the input slew of an input of the current gate from the output slew of the previous gate
            tau_in = prev_node.Tau_out

            # Calculate the input arrival of an input of the current gate from the output arrival of the previous gate
            input_arrival = prev_node.max_out_arrival
            node.inp_arrival.append(input_arrival)

            # Perform interpolation calculations
            gate_delay = interpolate_arrays(tau_in, node.Cload, slew_array, cap_array, gate_delay_array)
            gate_slew  = interpolate_arrays(tau_in, node.Cload, slew_array, cap_array, gate_slew_array)

            # Calculate delay and slew based on an n-input gate
            if num_inputs > 2:
                scale_lut = num_inputs / 2.0
                gate_delay *= scale_lut
                gate_slew *= scale_lut

            # Determine a_out = a_in + delay
            a_out = input_arrival + gate_delay

            # Add the gate_delay to a dictionary in the Node object to easily identify for backwards traversal later
            # keys = fanin gate names
            # values = gate_delay
            node.cell_delays[fan_in.name] = gate_delay

            # Add all a_out values to the outp_arrival times list for that node
            node.outp_arrival.append(a_out)

            # Determine a_out = max(a_in + delay)
            # Check to for each input to see which gives the max a_out
            if a_out > max_arrival_time:
                max_arrival_time = a_out
                fastest_slew = gate_slew

        # Now that all inputs have been checked and the max determined
        node.max_out_arrival = max_arrival_time
        node.Tau_out = fastest_slew


def backward_sta(nodes, ckt_delay, order):
    """
    Moves backward through the circuit END -> START to calculate the required time and slack of each node

    :param nodes: A dict that contains all node objects
    :param ckt_delay: Total delay of entire circuit (used as starting point for backwards STA)
    """

    required_arrival_time = 1.1 * ckt_delay  # Based on specs in document for 1.1 * delay

    order.reverse()                          # Reverses list order for backwards traversal

    # Iterate through gates from OUTPUTs to INPUTs in the circuit
    for gate in order:
        node = nodes[gate.name]

        if node.gate_type == 'OUTPUT':
            node.required_time = required_arrival_time  # Based on specs in document for 1.1 * delay for all outputs

        # Check all fanin for that gate to move back through the circuit
        for fan_in in node.fanin:
            prev_node = nodes[fan_in.name]

            # Used Codex to help fix the backwards traversal as I forgot to store the delay values for the fanin for each cell
            # Basically will either grab the value for that fanin from the cell_delay dict or it will give value of 0.0 if key doesn't exist
            cell_delay = node.cell_delays.get(fan_in.name, 0.0)

            # Comput the current nodes required time and subtract the cell delay from that fanin combination
            node_req = node.required_time - cell_delay

            # Grab required_time values from the LUT object and set to be minimum for the next node
            prev_node.required_time = min(node_req, prev_node.required_time)

    # Now that all inputs have been checked and the required times determined, calculate the slack
    for n in nodes.values():
        n.slack = n.required_time - n.max_out_arrival
        


def parse_bench(file, lut=None):
    """
    Parses the ckt.bench files to get circuit topology
    
    :param file: ckt.bench file
    :param lut: LUT object to be used for getting values from parsing nldm
    """
    inputs, outputs = [], []        # Creates lists to store the inputs/outputs of nodes (in this case ckt gates)
    nodes = {}                      # Creates dictionary to store all node objects
    gate_counter = defaultdict(int) # Creates dictionary to count the integer number of gates per type created
    gate_connections = []           # Will store tuples of gate_name, outputs, and inputs for future STA

    # Open ckt.bench file for reading and parse each line
    with open(file, 'r') as ckt_file:
        for line in ckt_file:
            line = line.strip()

            # Ignore commented lines
            if not line or line.startswith('#'):
                continue   # Moves to next line when reaching a comment or no entry

            # Identify Primary Inputs using regular expressions
            # Finds the \d+ decimal value character  connected to the enclosed ()
            if line.startswith('INPUT'):
                input_wire = re.findall(r'\((.*?)\)', line)[0]  # Finds the number identifier of the inputs - ex. INPUT(1) gets '1'
                inputs.append(input_wire)                       # Add to list to track number of primary inputs 
                input_name = f'INPUT-{input_wire}'

                # Create INPUT nodes for starting circuit
                # Checks to see if node has already been created, if not, adds it to netlist
                if input_name not in nodes:
                    nodes[input_name] = Node.Node(input_name, 'INPUT')
                    input_node = nodes[input_name]
                else:
                    input_node = nodes[input_name]

                # Set the initialized values for Tau_out and max_out_arrival based on assignment specifications when node is initialized
                input_node.outp_arrival.append(0.0)
                input_node.max_out_arrival = 0.0
                input_node.Tau_out = 0.002          # equal to 2ps based on how LUT is formatted

            # Identify Primary Inputs using regular expressions
            elif line.startswith('OUTPUT'):
                output_wire = re.findall(r'\((.*?)\)', line)[0]
                outputs.append(output_wire)
                output_name = f'OUTPUT-{output_wire}'

                # Create OUTPUT nodes for finishing circuit
                # Checks to see if node has already been created, if not, adds it to netlist
                if output_name not in nodes:
                    nodes[output_name] = Node.Node(output_name, 'OUTPUT')
                    output_node = nodes[output_name]
                else:
                    output_node = nodes[output_name]

            # When node is not a primary input/output
            elif ('=') in line:
                gate_name, gate = line.split('=')       # Splits at '=' so ex. gate_name is 10 '=' and gate is NAND(1,3)
                output_wire_name = gate_name.strip()

                # Finds the \w+ word character instance connected to the initial - ex. 'name('
                gate_type = re.findall(r'(\w+)\(', gate)[0]

                # Finds all values contained in paratheses and splits all inputs seperated by commas to get a list ['n1', 'n2', 'n3',...]
                input_wires = re.findall(r'\((.*?)\)', gate)[0].split(',')

                gate_name = f'{gate_type}-{output_wire_name}'   # Set gate name - ex. NAND-22

                # Checks to see if node has already been created, if not, adds it to netlist
                if gate_name not in nodes:
                    nodes[gate_name] = Node.Node(gate_name, gate_type)
                    node = nodes[gate_name]
                else:
                    node = nodes[gate_name]

                # Increment the number of gates of that type by 1 (uses this gate_type locally here to ensure that INPUTS/OUTPUTS are not added)
                gate_counter[gate_type] += 1

                # Connect gate inputs but will not fully connect them as objects since input gates come up later and was throwing errors
                # Fix of a list of tuples was suggested by codex
                gate_connections.append((gate_name, output_wire_name, input_wires))

            else:
                continue # Information not important for netlist creation
    

    connect_inputs(gate_connections, nodes)  # Connect all input nodes and set their fanin <-> fanout
    connect_outputs(outputs, nodes)          # Connect all output nodes in final fanout
    
    # Write all values to .txt file
    filename = str(file).replace('.', '_')
    output_filename = f'ckt_details_{filename}.txt'
    write_ckt_output(inputs, outputs, gate_counter, nodes, output_filename)   # Write to .txt file for ckt_bench parsing output

    
    ## START STA if the lut was parsed via command terminal ##
    if lut is not None:

        compute_cload(nodes, lut)   # Compute Cload of the gates by adding all Cin values from fanouts
        
        order = topological_order(nodes)         # Perform topological sorting for gates
        
        forward_sta(nodes, lut, order)     # Compute the forward STA to be able to calculate forward circuit delay


        ## Compute Total Circuit Delay
        delay = 0.0                 # Used to compute the max deley between all OUTPUT nodes
        output_node_list = []       # Will store all OUTPUT nodes in a list so that their slack values after backward_sta() can be compared to determine which one is 0 for the crit path

        # Will iterate through all created nodes and compare the max_out_arrival times for all OUTPUT nodes
        for n in nodes.values():
            if n.gate_type == 'OUTPUT':
                delay = max(delay, n.max_out_arrival)    # Chooses max between current max delay or max_out_arrival of current OUTPUT node
                output_node_list.append(n)               # Add all output nodes to a list to be used for critical path calculation
        

        backward_sta(nodes, delay, order)  # Compute the backward STA to be able to calculate forward slack and critcal path


        ## Compute Critical Path
        path = []                                                                    # List to store all node names in crit path
        crit_path_start = min(output_node_list, key=lambda out_node: out_node.slack) # Determines output with minimum output slack <- Codex syntax
        gate = crit_path_start                                                       # Start node chain

        # Will keep iterating backwards via the gates until there is an gate with not inputs (i.e. 'INPUT' node)
        while gate.fanin:
            fanin_n = [] # Stores all fanin nodes of a gate to check for min

            # Check all intputs for that gate
            for fan_in in gate.fanin:
                fanin_n.append(nodes[fan_in.name])  # Grabs the node object for that fanin

            # Once all fanin have been run through for that node, add that gate to the critical path and check for the fanin that
            # created the minimum slack and set that node as your next gate
            path.append(gate.name)
            gate = min(fanin_n, key=lambda in_node: in_node.slack)


        path.append(gate.name) # Used to make sure you Add INPUT node to critical path since it does not have a fanin
        path.reverse()         # Use to make sure that the critical path is read from INPUT -> OUTPUT

        write_ckt_traversal(delay, nodes, path, output_file=f'ckt_traversal_{filename}.txt')  # Write STA traversal output to file





# Main parser logic
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                            description='STA program to read circuit and nldm library files')

    # Add arguments to created line command
    # py parser.py --read_ckt c17.bench
    parser.add_argument('--read_ckt', type=pathlib.Path, help='Create path to ckt.bench file')

    # py parser.py --delays --read_nldm sample_NLDM.lib
    # py parser.py --slews --read_nldm sample_NLDM.lib
    parser.add_argument('--read_nldm', type=pathlib.Path, help='Create path to nldm .library file')
    parser.add_argument('--delays', action='store_true', help='Solves for delays in nldm file')
    parser.add_argument('--slews', action='store_true', help='Solves for output slews in nldm file')

    args = parser.parse_args() # Will grab all created command arguements
    #print(args) # Sanity check
    
    lut = None    # In case you are only parsing and not doing STA
    mode = None   # In case you are doing STA

    # Check argument is called/exists and if library file exists
    if args.read_nldm:
        if args.read_nldm.is_file():
            lut = LUT.LUT()
            if args.delays:
                mode = 'delays'
                lut.parse_nldm(args.read_nldm, mode) # Calls function to parse .lib file for --delays
            elif args.slews:
                mode = 'slews'
                lut.parse_nldm(args.read_nldm, mode)  # Calls function to parse .lib file for --slews
            else:
                lut.parse_nldm(args.read_nldm, mode)

        else:
            print(f'Error: NLDM file not found - {args.read_nldm}')

    
    # Check if argument is called/exists and if circuit file exists
    # Have to put this after read_nldm for STA to work!!
    if args.read_ckt:
        if args.read_ckt.is_file():
            parse_bench(args.read_ckt, lut) # Calls function to parse ckt.bench file
        else:
            print(f'Error: Circuit file not found - {args.read_ckt}')

