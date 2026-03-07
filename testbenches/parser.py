################################################################################
# Assignment : Mini-Project 1 - Phase 1                                        #
# Team: Ctrl Freaks                                                            #
# ---------------------------------------------------------------------------  #
#                                                                              #
# Parser File to Read circuits using Node class and NLDM library files         #
# using LUT class to generate the netlist and get gate info into txt files     #
# to traverse the circuit and calculate delays and critical path.              #
################################################################################

# All automatically in python 3.7 in theory
import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict
from collections import deque


class Node:
    def __init__(self, gate_name, gate_type=None):
        """
        Creates a class NODE to represent the different verticies in the circuit
        
        :param self: Used to call local variables of class NODE
        :param gate_name: Represents the name of the input/output of a node
        :param gate_type: Represents the type of logic gate in the circit
        """
        self.name = gate_name      # Gives the name with the gate_type and coresponding number
        self.gate_type = gate_type # Specifes the gate function (ex. INPUT, NOR, INV, NAND)

        self.Cload = 0.0           # Gives output capacitance of the gate

        self.fanin = []            # list of handles to the fanin nodes of this node
        self.fanout =[]            # list of handles to the fanout nodes of this node

        self.Tau_in = []           # array/list of input slews (for all inputs to the gate), to be used for STA
        self.inp_arrival = []      # array/list of input arrival times for input transitions (ignore rise or fall)
        self.outp_arrival = []     # array/list of output arrival times, outp_arrival = inp_arrival + cell_delay
        self.max_out_arrival = 0.0 # arrival time at the output of this gate using max on (inp_arrival + cell_delay)
        self.Tau_out = 0.0         # Resulting output slew

        self.slack = 0.0
        self.required_time = float('inf')
        self.cell_delays = {}

class LUT:
    def __init__(self):
        """
        Creates a class LUT to represent the different cells in the nldm library file
        
        :param self: Used to call local variables of class LUT
        """
        self.full_cell = {}             # Dictionary to store all cells based on name with a nested dictionary to hold all the values

        self.Allgate_name = []          # all cells defined in the LUT
        self.Cin = []                   # capacitance of each cell
        self.All_delays = np.array([])  # 2D numpy array delay LUTs for each cell
        self.All_slews = np.array([])   # 2D numpy array to store output slew LUTs for each cell
        self.Cload_vals = np.array([])  # 1D numpy array corresponds to the 2nd index in the LUT
        self.Tau_in_vals = np.array([]) # 1D numpy array corresponds to the 1st index in the LUT
    
    
    
    def write_nldm_output(self, delay_or_slew, output_file):
        """
        Prints the output .txt file from reading the nldm .li file

        :param mode: Determines if the parser argument of --delays or --slews was used (Determines whether the command line prompt wants to calculate delay or slew)
        :param output_file: Gives the name of the .txt to write to
        """

        # Open output nldm file for writing line by line
        with open(output_file, 'w') as nldm_file:

            # Go through every cell in he dictionary of format Cell { Cell_name {all cell parameters or cell_data} }
            for cell_name, cell_data in self.full_cell.items():

                nldm_file.write(f'cell: {cell_name} \n')            # Print cell name (ex. NAND) to file

                slews = ','.join(map(str, cell_data['index_1']))    # Add every value from 1D array together and seperate them by commas
                caps = ','.join(map(str, cell_data['index_2']))

                nldm_file.write(f'input slews: {slews} \n')         # Print index_1 and index_2 to file
                nldm_file.write(f'load cap: {caps} \n')

                # When arguement is --delays
                if (delay_or_slew == 'delays'):
                    nldm_file.write(f'\n{delay_or_slew}: \n')
                    
                    for row in cell_data['delays']:                 # Should print cell_delays row by row from the 2D array and seperate them by commas
                        times = ','.join(map(str, row))
                        nldm_file.write(f'{times}; \n\n')

                # When arguement is --slews
                elif (delay_or_slew == 'slews'):
                    nldm_file.write(f'\n{delay_or_slew}: \n')
                    
                    for row in cell_data['slews']:                  # Should print output_slew row by row from the 2D array and seperate them by commas
                        times = ','.join(map(str, row))
                        nldm_file.write(f'{times}; \n\n')
                
                # Shouldn't reach this point of if the argument is --delays or --slews
                # If no argument is included it should just end the program
                else:
                    print(f'Did not specify delay or slew for --read_ndlm')
                    exit(1)

                nldm_file.write(f'\n\n') # Add space between cells in txt file for formatting/reading



    def assign_arrays(self, cell_name, cell_input_cap, cell_input_slew, cell_cap_loads, cell_delays, cell_slews):
        """
        Will be used for future math in circuit traversal calculations
        
        :param cell_name: Description
        :param cell_input_cap: Description
        :param cell_input_slew: Description
        :param cell_cap_loads: Description
        :param cell_delays: Description
        :param cell_slews: Description
        """
        # I was thinking for the math since we have to use the netlist and such we could have a condition to check if gate_num_inputs > 2 and 
        # if so, then use a equation to multiply all delay and slew array values by n
        self.Allgate_name = [cell_name]                # all cells defined in the LUT
        self.Cin = [cell_input_cap]                    # capacitance of each cell
        self.All_delays = np.array([cell_delays])      # 2D numpy array delay LUTs for each cell
        self.All_slews = np.array([cell_slews])        # 2D numpy array to store output slew LUTs for each cell
        self.Cload_vals = np.array([cell_cap_loads])   # 1D numpy array corresponds to the 2nd index in the LUT
        self.Tau_in_vals = np.array([cell_input_slew]) # 1D numpy array corresponds to the 1st index in the LUT


    def parse_nldm(self, file, delay_or_slew=None):
        """
        Reads the .lib file and uses regualr expressions to identify and grab different sections of text within the file for arrays

        :param file: nldm .library file
        :param delay_or_slew: Determines if the parser argument of --delays or --slews was used (Determines whether the command line prompt wants to calculate delay or slew)
        """

        with open(file, 'r') as lib_file:
            file_txt = lib_file.read()  # Reads entire file to then edit off of using regular expressions
            
        # (.*?) - used to capture all characters within a specific range greedily and \s* ignores all white space and make it a group
        # re.S used since it is a multi-line operation with findall() giving all cell instances in a list
        # Creates 4 total groups to store diffrent values to use in the for loop
        cell_body = re.findall(r"cell\s*\(\s*(.*?)\)\s*\{(.*?);\n\s*(.*?)\}\s*.*?\{(.*?)\n\s*\}", file_txt, re.S) # Can grab all cells and entire body just in different groups!!
        #print(f'body: {cell_body}\n\n')

        for cell, cap, delay, slew in cell_body:
            cell_values = {}              # dictionary to store all future array values
            
            #print(f'cell: {cell}\n')     # ex. cell: INVx1
            #print(f'cap: {cap}\n')       # cap:     capacitance             : 1.700230
            #print(f'data: {delay}\n')    # data: cell_delay(Timing_7_7) {...}
            #print(f'data: {slew}\n')     # data: index_1(...); index_2(...); values(2D array)

            # ([\d\.]+) - captures all digit values including the decimal for the decimal number assuming there is at least 1 number
            # [0] - grabs the value from the list instead of just returning a list with the value in it
            cap_value = re.findall(r'capacitance\s*:\s*([\d\.]+)', cap)[0]
            cell_capacitance = float(cap_value)
            #print(f'caps: {cap_value}\n\n')

            # Extract cell delay values (index 1 and 2 are to be the same regardless of delay or slew)
            index_1 = re.findall(r'index_1\s*\("(.*?)"\)', delay)[0]
            index_2 = re.findall(r'index_2\s*\("(.*?)"\)', delay)[0]
            delay_values = re.findall(r'values\s*\((.*?)\);', delay, re.S)[0] # Has the entire list and will need to parse for valures
            slew_values = re.findall(r'values\s*\((.*?)\);', slew, re.S)[0]   # Has the entire list and will need to parse for valures

            #print(f'index_1: {index_1}\n')
            #print(f'index_2: {index_2}\n')
            #print(f'delay: {delay_values}\n')
            #print(f'slew: {slew_values}\n')

            # Create 1D arrays of size 7 to store different tau and load_cap values
            tau_values = np.zeros(7)
            load_cap_values = np.zeros(7)

            # Use to track integer position in np.array to add slew values to specific 1D array index
            index = 0
            for tau in index_1.split(','):
                tau_values[index] = float(tau)
                index += 1

            index = 0
            for load_cap in index_2.split(','):
                load_cap_values[index] = float(load_cap)
                index += 1

            #print(f'taus: {tau_values}\n\n')
            #print(f'load caps: {load_cap_values}\n\n')

            # Parse delay and slew and get rid of all tab, newline, and \ characters that would complicate parsing
            delay_time = delay_values.replace('\\', '').replace('\n','').replace('\t','')
            slew_time = slew_values.replace('\\', '').replace('\n','').replace('\t','')

            #print(f'delay after replacing: {delay_time}\n')
            #print(f'slew after replacing: {slew_time}\n')

            # Put row by row into a list format to access each as needed
            delay_rows = re.findall(r'"(.*?)"', delay_time, re.S)
            slew_rows = re.findall(r'"(.*?)"', slew_time, re.S)
            
            #print(f'delay rows {delay_rows}\n')
            #print(f'slew rows {slew_rows}\n')

            # Set size of array to 7 by 7 as per project instructions
            delay_array = np.zeros((7,7)) # Make 2D arrary for delay
            slew_array = np.zeros((7,7)) # Make 2D arrary for slew
            
            # Use to track integer position in np.array to add slew values to specific 2D array index
            array_position_row = 0
            array_position_col = 0

            for row in delay_rows:
                for col in row.split(','):
                    delay_array[array_position_row][array_position_col] = float(col)
                    array_position_col += 1

                array_position_row += 1
                array_position_col = 0 # Reset columns to not go out of index

            #print(f'final delay array: {delay_array}\n\n')

            # Use to track integer position in np.array to add slew values to specific 2D array index
            array_position_row = 0
            array_position_col = 0

            # Run through slew values in each row and split into columns using commas
            for row in slew_rows:
                for col in row.split(','):
                    slew_array[array_position_row][array_position_col] = float(col)
                    array_position_col += 1

                array_position_row += 1
                array_position_col = 0 # Reset columns to not go out of index

            #print(f'final slew array: {slew_array}\n\n')

            # Creates dictionary to store input cap, delay, and slew values
            cell_values = {
                'input_cap': cell_capacitance,
                'index_1': tau_values,
                'index_2': load_cap_values,
                'delays': delay_array,
                'slews': slew_array
            }

            self.full_cell[cell] = cell_values
            #print(cell_values)
            #print(self.full_cell)

            ## NEED TO ADD THE WAY TO CALCULATE THE TIME VALUES BASED ON THE 2D ARRARY!!!!
            self.assign_arrays(cell,
                               cell_values['input_cap'],
                               cell_values['index_1'],
                               cell_values['index_2'],
                               cell_values['delays'],
                               cell_values['slews']
                               )


        # Write all values to .txt file
        if (delay_or_slew == 'delays'):
            output_filename = 'delay_LUT.txt'
            self.write_nldm_output(delay_or_slew, output_filename)   # Write to .txt with assignment format

        elif (delay_or_slew == 'slews'):
            output_filename = 'slew_LUT.txt'
            self.write_nldm_output(delay_or_slew, output_filename)   # Write to .txt with assignment format




def connect_inputs(gate_connections, nodes: dict):
    """
    Connects the primary inputs and mid-level gate inputs in the circuit
    
    :param input_wires: Represents the inputs to a node/vertice
    :param nodes: Represnts the object node
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """

    ckt_wires = {}

    for n in nodes.values():
        wire = n.name.split('-')[-1]
        ckt_wires[wire] = n

    # Checks all inputs for that node against the node values to determine where they are in circuit
    for gate_n, output_w, input_w in gate_connections:

        gate_node = nodes[gate_n]
        #print(f'\ngate_node : {gate_node.name}\n')

        for w in input_w:
            input = w.strip()
            input_node = ckt_wires[input]
            #print(f'\ninput_node : {input_node.name}\n')
            #print(f'\ngate_tau_out : {input_node.Tau_out}\n')

            # Add all fanin and fanouts to circuit - need to use node.name otherwise it will add the Node object and not a string (made issues in printing)
            gate_node.fanin.append(input_node)   # Input -> Node
            input_node.fanout.append(gate_node)  # Input <- Node


            #print(f'\nafter connected input node name {vars(gate_node)}\n')
            #print(f'\nafter connected input node name {vars(input_node)}\n')




def connect_outputs(output_wires, nodes: dict):
    """
    Connects final outputs of the circuit
    
    :param output_wires: Represents the outputs of a node/vertice
    :param nodes: Represnts the object node
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """
    
    # Checks all output_wires against the node values to determine where they are in circuit
    for output in output_wires:

        output_name = f'OUTPUT-{output}'

        #if output_name not in nodes:
        #    nodes[output_name] = Node(output_name, 'OUTPUT')
        #    output_node = nodes[output_name]
        #else:
        output_node = nodes[output_name]

        for node in nodes.values():

            if node.gate_type == 'OUTPUT':
                continue

            # If output is only connected to a number, replace it with OUTPUT-that number
            if node.name.endswith(f'-{output}'):
                #output_name = f'OUTPUT-{output}'
                #output_node = Node(output_name, 'OUTPUT') # Creates new OUTPUT node type
                
                # Add all fanin and fanouts to circuit - need to use node.name otherwise it will add the Node object and not a string (made issues in printing)
                node.fanout.append(output_node) # Node -> Output
                output_node.fanin.append(node)  # Node <- Output

                #print(f'\nafter connected output node name {vars(node)}\n')
                #print(f'\nafter connected output node name {vars(output_node)}\n')




# Officially works!!!!!!!
def write_ckt_output(ckt_inputs, ckt_outputs, gate_counter, nodes, output_file='ckt_details.txt'):
    """
    Prints the netlist file as described in appendix 1
    
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
            if not ((node.gate_type == 'INPUT') or (node.gate_type == 'OUTPUT')):
                fanout_values = []

                # Iterate through all fanout values
                for n in node.fanout:
                    fanout_values.append(n.name)

                # Write all fanout node pairs and use .join concatinate all output node names
                #print(f'fanout : {fanout_values}')
                ckt_file.write(f'{node.name}: ' + ', '.join(fanout_values) + '\n')
                #print(f'{node.name}: ' + ', '.join(fanout_values) + '\n')


        # Fanin of specific gates
        ckt_file.write('\nFanin...\n')
        # Iterate through all node values
        for node in nodes.values():
            if not (node.gate_type == 'INPUT'):
                fanin_values = []

                # Iterate through all fanout values
                for n in node.fanin:
                    fanin_values.append(n.name)

                # Write all fanout node pairs and use .join concatinate all input node names
                ckt_file.write(f'{node.name}: ' + ', '.join(fanin_values) + '\n')
                #print(f'{node.name}: ' + ', '.join(fanin_values) + '\n')


def write_ckt_traversal(ckt_inputs, ckt_outputs, ckt_delay, nodes, path, output_file='ckt_traversal.txt'):
    """
    Prints the output of traversal calculations as described in appendix 2
    
    :param output_file: Gives the name of the .txt to write to
    """

    # Open output circuit file for writing line by line
    with open(output_file, 'w') as ckt_file:
        ckt_file.write(f'Circuit delay: {ckt_delay * 1000:.5f} ps\n')

        # Fanout of specific gates
        ckt_file.write('\nGate slacks:\n')

        # Iterate through all node values and Write all node names and output slack at each node
        for node in nodes.values():
            ckt_file.write(f'{node.name}: {node.slack * 1000:.5f} ps\n')

        ckt_file.write(f'\nCritical path:\n')
        ckt_file.write(f'\n' + ', '.join(path) + '\n')



def compute_cload(nodes, lut):

    # Iterate through all node values
    for node in nodes.values():
        total_cap = 0.0

        if node.gate_type in ['INPUT', 'OUTPUT']:
            continue

        for fan_o in node.fanout:
            #print(f'\nafter connected output node name {vars(node)}\n')
            #print(f'\noutput node name {fan_o.name}\n')
            #print(f'\n nodes : {nodes}\n')
            fanout_n = fan_o

            if fanout_n.gate_type == 'OUTPUT':
                total_cap += 4 * lut.full_cell['INV_X1']['input_cap']
            else:
                if fanout_n.gate_type == 'BUFF':
                    gate_name = 'BUF_X1'
                elif fanout_n.gate_type == 'NOT':
                    gate_name = 'INV_X1'
                else:
                    gate_name = fanout_n.gate_type + '2_X1'


                total_cap += lut.full_cell[gate_name]['input_cap']

        node.Cload = total_cap


def interpolate_arrays(slew_row, cap_col, xvals, yvals, array_2d_vals):

        x = np.searchsorted(xvals, slew_row) - 1
        y = np.searchsorted(yvals, cap_col)  - 1

        # Was having bounds issues and Codex gave the following two lines as a solution
        # -2 makes it so that x+1 and y+1 are valid
        x = max(0, min(x, len(xvals)-2))
        y = max(0, min(y, len(yvals)-2))

        print(f'\nx : {x}')
        print(f'y : {y}')

        slew1, slew2   = xvals[x], xvals[x+1]
        #cap1, cap2     = xvals[x], xvals[x+1]
        #slew1, slew2   = yvals[y], yvals[y+1]
        cap1, cap2     = yvals[y], yvals[y+1]

        print(f'slews : {slew1}   {slew2}')
        print(f'caps  : {cap1}    {cap2}')

        v11 = array_2d_vals[x][y]
        v12 = array_2d_vals[x][y+1]
        v21 = array_2d_vals[x+1][y]
        v22 = array_2d_vals[x+1][y+1]

        print(f'v11 : {v11}')
        print(f'v12 : {v12}')
        print(f'v21 : {v21}')
        print(f'v22 : {v22}')

        print(f'cap2 {cap2}   cap_col {cap_col}   to {cap2 - cap_col}')
        print(f'slew2 {slew2}   slew_row {slew_row}   to {slew2 - slew_row}')

        print(f'cap_col {cap_col}   cap1 {cap1}   to {cap_col - cap1}')
        print(f'slew_row {slew_row}   slew1 {slew1}   to {slew_row - slew1}\n')

        numerator = (v11 * (cap2 - cap_col)*(slew2 - slew_row)) + (v12 * (cap_col - cap1)*(slew2 - slew_row)) + (v21 * (cap2 - cap_col)*(slew_row - slew1)) + (v22 * (cap_col - cap1)*(slew_row - slew1))
        denominator = (cap2 - cap1) * (slew2 - slew1)


        interpolated_value = numerator / denominator
        print(interpolated_value)

        return interpolated_value


def topological_order(nodes):
    # Used geeksforgeeks as baseline for topological sort (https://www.geeksforgeeks.org/dsa/topological-sorting-indegree-based-solution/)
    gate_order = []
    indegree = {}
    queue = deque()

    # Compute indegrees for each node
    for node in nodes.values():
        print(f'node names : {node.name}')
        indegree[node.name] = len(node.fanin)

        if indegree[node.name] == 0:
            queue.append(node)


    print(f'idegrees : {indegree[node.name]}')
    print(f'queue : {queue}')

    # Kahn’s Algorithm
    while queue:
        node = queue.popleft()       # Pop the first node on the queue
        gate_order.append(node)  # Add node to visited nodes in the gate order
        print(f'gate order : {node.name}')

        # Check all connected nodes via the fanout
        for next_node in node.fanout:
            #print(f'indegree : {indegree}')
            indegree[next_node.name] -= 1 # Subtract the indegree of next_node since others were processed

            print(f'next_node : {next_node.name}')
            print(f'idegrees : {indegree[next_node.name]}')

            # If next_node is connected to previous node
            if indegree[next_node.name] == 0:
                queue.append(next_node)

    return gate_order


def forward_sta(nodes, lut):

    order = topological_order(nodes)
    print(f'\norder : {order}')

    for gate in order:
        node = nodes[gate.name]

        print(f'\n\nnode {vars(node)}\n\n')

        if node.gate_type == 'INPUT':
            continue

        if node.gate_type == 'OUTPUT':
            prev_node = node.fanin[0]  # Identifies sole fanin for output
            node.max_out_arrival = prev_node.max_out_arrival
            node.inp_arrival.append(node.max_out_arrival)
            node.outp_arrival.append(node.max_out_arrival)

            print(f'node : {node.name}')
            print(f'node : {node.max_out_arrival}')
            print(f'\n\nnode {vars(node)}\n\n')
            continue

        max_arrival_time, fastest_slew = 0.0, 0.0

        for fan_in in node.fanin:
            prev_node = nodes[fan_in.name]

            print(f'prev_node {vars(prev_node)}\n')

            if node.gate_type == 'BUFF':
                    gate_name = 'BUF_X1'
            elif node.gate_type == 'NOT':
                gate_name = 'INV_X1'
            else:
                gate_name = node.gate_type + '2_X1'

            # Calculate the input slew of an input of the current gate from the output slew of the previous gate
            tau_in = prev_node.Tau_out

            # Calculate the input arrival of an input of the current gate from the output arrival of the previous gate
            input_arrival = prev_node.max_out_arrival
            node.inp_arrival.append(input_arrival)

            # Grab values from the LUT object
            slew_array = lut.full_cell[gate_name]['index_1']
            cap_array = lut.full_cell[gate_name]['index_2']
            gate_delay_array = lut.full_cell[gate_name]['delays']
            gate_slew_array = lut.full_cell[gate_name]['slews']

            print(f'delays : {gate_delay_array}')
            print(f'slews : {gate_slew_array}')

            # Perform interpolation calculations
            gate_delay = interpolate_arrays(tau_in, node.Cload, slew_array, cap_array, gate_delay_array)

            gate_slew  = interpolate_arrays(tau_in, node.Cload, slew_array, cap_array, gate_slew_array)

            # Determine a_out = a_in + delay
            a_out = input_arrival + gate_delay

            node.cell_delays[fan_in.name] = gate_delay

            #print(f'cell_delay : {node.cell_delays}')

            node.outp_arrival.append(a_out)
            print(f'a_out : {a_out}')
            print(f'delay : {gate_delay}')
            print(f'input_arrival : {input_arrival}')

            # Determine a_out = max(a_in + delay)
            # Check to for each input to see which gives the max a_out
            if a_out > max_arrival_time:
                max_arrival_time = a_out
                fastest_slew = gate_slew

            print(f'max_arrival_time : {max_arrival_time}')
            print(f'fastest_slew : {fastest_slew}')
            print(f'\nfanin {fan_in.name}\n\n')

        print(f'\n\nnode {node.name}\n\n')

        # Now that all inputs have been checked and the max determined
        node.max_out_arrival = max_arrival_time
        node.Tau_out = fastest_slew

        print(f'\n\nnode {vars(node)}\n\n')
        print(f'cell_delay : {node.cell_delays}')






def backward_sta(nodes, ckt_delay):

    required_arrival_time = 1.1 * ckt_delay  # Based on specs in document for 1.1 * delay

    order = topological_order(nodes)
    order.reverse()   # Reverses list order for backwards traversal

    for gate in order:
        node = nodes[gate.name]

        print(f'\n\nnode name backwards {gate.name}\n\n')
        print(f'\n\nnode  backwards {vars(node)}\n\n')

        if node.gate_type == 'OUTPUT':
            node.required_time = required_arrival_time

        for fan_in in node.fanin:
            prev_node = nodes[fan_in.name]

            cell_delay = node.cell_delays.get(fan_in.name, 0.0)

            node_req = node.required_time - cell_delay

            # Grab slack values from the LUT object
            #prev_node.required_time = min(node.required_time, prev_node.required_time)
            prev_node.required_time = min(node_req, prev_node.required_time)

            print(f'prev required : {prev_node.required_time}')
            print(f'curr required : {node.required_time}')

            print(f'\n\nnode {vars(node)}\n\n')

    # Now that all inputs have been checked and the required times determined, calculate the slack
    for n in nodes.values():
        n.slack = n.required_time - n.max_out_arrival
        
        print(f'node :: {n.name}')
        print(f'slack :: {n.slack}')

    #exit(1)



def parse_bench(file, lut=None):
    """
    Parses the ckt.bench files to get circuit topology
    
    :param file: ckt.bench file
    """
    inputs, outputs = [], []        # Creates lists to store the inputs/outputs of nodes (in this case ckt gates)
    nodes = {}                      # Creates dictionary to store all node objects
    gate_counter = defaultdict(int) # Creates dictionary to count the integer number of gates per type created

    gate_connections = []

    # Open ckt.bench file for reading and parse each line
    with open(file, 'r') as ckt_file:
        for line in ckt_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue   # Moves to next line when reaching a comment or no entry

            # Identify Inputs using regular expressions
            # Finds the \d+ decimal value character  connected to the enclosed ()
            if line.startswith('INPUT'):
                input_wire = re.findall(r'\((.*?)\)', line)[0]
                #print(f'input_wire {input_wire}')
                inputs.append(input_wire)
                input_name = f'INPUT-{input_wire}'

                # Create INPUT nodes for starting gates
                # Checks to see if node has already been created, if not, adds it to netlist
                if input_name not in nodes:
                    nodes[input_name] = Node(input_name, 'INPUT')
                    input_node = nodes[input_name]
                else:
                    input_node = nodes[input_name]

                input_node.outp_arrival.append(0.0)
                input_node.max_out_arrival = 0.0
                input_node.Tau_out = 0.002 # 2ps

            elif line.startswith('OUTPUT'):
                output_wire = re.findall(r'\((.*?)\)', line)[0]
                #print(f'output_wire {output_wire}')
                outputs.append(output_wire)
                output_name = f'OUTPUT-{output_wire}'
                print(output_name)

                if output_name not in nodes:
                    nodes[output_name] = Node(output_name, 'OUTPUT')
                    output_node = nodes[output_name]
                else:
                    output_node = nodes[output_name]

            # When node is not a primary input/output
            elif ('=') in line:
                gate_name, gate = line.split('=')       # Splits at '=' so ex. gate_name is 10 '=' and gate is NAND(1,3)
                output_wire_name = gate_name.strip()

                # Finds the \w+ word character instance connected to the initial ( ex. 'name('
                gate_type = re.findall(r'(\w+)\(', gate)[0]

                # Finds all values contained in paratheses and splits all inputs seperated by commas to get a list ['n1', 'n2', 'n3',...]
                input_wires = re.findall(r'\((.*?)\)', gate)[0].split(',')
                #print(f'\ninput_wires {input_wires}')

                gate_name = f'{gate_type}-{output_wire_name}'
                #print(f'gate name {gate_name}')

                # Checks to see if node has already been created, if not, adds it to netlist
                if gate_name not in nodes:
                    nodes[gate_name] = Node(gate_name, gate_type)
                    node = nodes[gate_name]
                else:
                    node = nodes[gate_name]

                #print(f'node {vars(node)}')

                # Increment the number of gates of that type by 1
                gate_counter[gate_type] += 1

                # Connect gate inputs but will not fully connect them since gates come up later and I don't want to assign them at the wrong time by accident
                gate_connections.append((gate_name, output_wire_name, input_wires))

            else:
                continue # Information not important for netlist creation
    

    connect_inputs(gate_connections, nodes)
    
    # Connect all output nodes in fanout
    connect_outputs(outputs, nodes)
    
    # Write all values to .txt file
    filename = str(file).replace('.', '_')
    output_filename = f'ckt_details_{filename}.txt'
    write_ckt_output(inputs, outputs, gate_counter, nodes, output_filename)

    
    ## START STA ##
    if lut is not None:

        compute_cload(nodes, lut)

        #for n in nodes.values():
        #    print(f'\nname : {n.name}')
        #    print(f'tau_out : {n.Tau_out}')
        #    print(f'Cload : {n.Cload}')

        forward_sta(nodes, lut)


        # Compute Total Circuit Delay
        delay = 0.0
        output_node_list = []

        for n in nodes.values():
            if n.gate_type == 'OUTPUT':
                delay = max(delay, n.max_out_arrival)
                output_node_list.append(n)
        
        backward_sta(nodes, delay)

        # Compute Critical Path
        path = []                                                                    # List to store all node names in crit path
        crit_path_start = min(output_node_list, key=lambda out_node: out_node.slack) # Determines output with minimum output slack
        
        gate = crit_path_start # Start node chain

        # Will keep iterating backwards via the gates until there is an gate with not inputs (i.e. 'INPUT' node)
        while gate.fanin:
            fanin_n = [] # Stores all fanin nodes of a gate to check for min

            # Check all intputs for that gate
            for fan_in in gate.fanin:
                fanin_n.append(nodes[fan_in.name])  # Grabs the object of 
            
            #print(f'fanin nodes : {fanin_n}')

            path.append(gate.name)
            gate = min(fanin_n, key=lambda in_node: in_node.slack)


        path.append(gate.name) # Add INPUT node
        path.reverse()         # Use to make sure that the critical path is read from INPUT -> OUTPUT 

        write_ckt_traversal(inputs, outputs, delay, nodes, path, output_file=f'ckt_traversal_{filename}.txt')







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
    
    lut = None # In case you are only parsing and not doing STA
    mode = None


    # Check argument is called/exists and if library file exists
    if args.read_nldm:
        if args.read_nldm.is_file():
            lut = LUT()
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


    print(f'LUT : {vars(lut)}\n\n')
    print(f'key : {list(lut.full_cell.keys())}')
    #exit(1)
    
    # Check if argument is called/exists and if circuit file exists
    if args.read_ckt:
        if args.read_ckt.is_file():
            parse_bench(args.read_ckt, lut) # Calls function to parse ckt.bench file
        else:
            print(f'Error: Circuit file not found - {args.read_ckt}')

