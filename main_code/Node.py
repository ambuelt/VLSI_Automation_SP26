################################################################################
# Assignment : Mini-Project 1 - Phase 1                                        #
# Team: Ctrl Freaks                                                            #
# ---------------------------------------------------------------------------  #
#                                                                              #
# Parser File to Read circuits using Node class and NLDM library files         #
################################################################################

# All automatically in python 3.7 terminal except for numpy and pathlib
import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict
from collections import deque

class Node:
    def __init__(self, gate_name, gate_type=None):
        """
        Creates a class NODE to represent the different gates in the circuit
        
        :param self: Used to call local variables of class NODE
        :param gate_name: Represents the name of the input/output of a node
        :param gate_type: Represents the type of logic gate in the circit
        """
        self.name = gate_name               # Gives the name with the gate_type and coresponding number
        self.gate_type = gate_type          # Specifes the gate function (ex. INPUT, NOR, INV, NAND)

        self.Cload = 0.0                    # Gives output capacitance of the gate

        self.fanin = []                     # list of handles to the fanin nodes of this node
        self.fanout =[]                     # list of handles to the fanout nodes of this node

        self.Tau_in = []                    # array/list of input slews (for all inputs to the gate), to be used for STA
        self.inp_arrival = []               # array/list of input arrival times for input transitions (ignore rise or fall)
        self.outp_arrival = []              # array/list of output arrival times, outp_arrival = inp_arrival + cell_delay
        self.max_out_arrival = 0.0          # arrival time at the output of this gate using max on (inp_arrival + cell_delay)
        self.Tau_out = 0.0                  # Resulting output slew

        self.slack = 0.0                    # Slack for each gate (slack = required_time - max_arrival_time)
        self.required_time = float('inf')   # Has all required times of the gates start as infinity so the decimal values will always be min in comparison
        self.cell_delays = {}               # Stores the internal delay of the cell from a specific fanin input (think like Figure 1 internal lines d1, d2...)
