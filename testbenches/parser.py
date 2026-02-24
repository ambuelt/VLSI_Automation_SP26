################################################################################
# Assignment : Mini-Project 1 - Phase 1                                        #
# Team: Ctrl Freaks                                                            #
# ---------------------------------------------------------------------------  #
#                                                                              #
# Parser File to Read circuits using Node class and NLDM library files         #
# using LUT class to generate the netlist and get gate info into txt files     #
# to traverse the circuit and calculate delays and critical path.              #
################################################################################

import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict


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

        self.Cload = 0.0           # Gives input capacitance of the gate

        self.fanin = []            # list of handles to the fanin nodes of this node
        self.fanout =[]            # list of handles to the fanout nodes of this node

        self.Tau_in = []           # array/list of input slews (for all inputs to the gate), to be used for STA
        self.inp_arrival = []      # array/list of input arrival times for input transitions (ignore rise or fall)
        self.outp_arrival = []     # array/list of output arrival times,outp_arrival = inp_arrival + cell_delay
        self.max_out_arrival = 0.0 # arrival time at the output of this gate using max on (inp_arrival + cell_delay)
        self.Tau_out = 0.0         # Resulting output slew

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


    def parse_nldm(self, file, delay_or_slew):
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
        elif (delay_or_slew == 'slews'):
            output_filename = 'slew_LUT.txt'
        else:
            print(f'Something went wrong???')
            exit(1)

        self.write_nldm_output(delay_or_slew, output_filename)   # Write to .txt with assignment format




def connect_inputs(input_wires, ckt_inputs, node, nodes: dict):
    """
    Connects the primary inputs and mid-level gate inputs in the circuit
    
    :param input_wires: Represents the inputs to a node/vertice
    :param nodes: Represnts the object node
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """

    # Checks all inputs for that node against the node values to determine where they are in circuit
    for input in input_wires:
        input = input.strip()

        # If the input is a primary input of type INPUT
        if input in ckt_inputs:
            input_node = nodes[f'INPUT-{input}']

        # If it's just a general gate -> gate input
        else:
            for n in nodes.values():
                if n.name.endswith(f'-{input}'):
                    input_node = n

        # Add all fanin and fanouts to circuit - need to use node.name otherwise it will add the Node object and not a string (made issues in printing)
        node.fanin.append(input_node.name)   # Input -> Node
        input_node.fanout.append(node.name)  # Input <- Node


def connect_outputs(output_wires, nodes: dict):
    """
    Connects final outputs of the circuit
    
    :param output_wires: Represents the outputs of a node/vertice
    :param nodes: Represnts the object node
    :type nodes: Represents the dictionary of all node object instances with all the parameters to use
    """
    
    # Checks all output_wires against the node values to determine where they are in circuit
    for output in output_wires:
        for node in nodes.values():

            # If output is only connected to a number, replace it with OUTPUT-that number
            if node.name.endswith(f'-{output}'):
                output_node = Node(f'OUTPUT-{output}', 'OUTPUT') # Creates new OUTPUT node type
                
                # Add all fanin and fanouts to circuit - need to use node.name otherwise it will add the Node object and not a string (made issues in printing)
                node.fanout.append(output_node.name) # Node -> Output
                output_node.fanin.append(node.name)  # Node <- Output



def write_ckt_traversal(ckt_inputs, ckt_outputs, gate_counter, nodes, output_file='ckt_traversal.txt'):
    """
    Prints the output of traversal calculations as described in appendix 2
    
    :param output_file: Gives the name of the .txt to write to
    """

    # Open output circuit file for writing line by line
    with open(output_file, 'w') as ckt_file:
        ckt_file.write(f'Circuit delay: {len(ckt_inputs)}\n')

        # Fanout of specific gates
        ckt_file.write('Gate slacks:\n')

        # Iterate through all node values and Write all node names and output slack at each node
        for node in nodes.values():
            ckt_file.write(f'{node.name}: {node.max_out_arrival}\n')

        ckt_file.write(f'Critical path:\n')

        # NEED TO DO: Print critical path from calculated values




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
            if not (node.gate_type == 'INPUT'):
                fanout_values = []

                # Iterate through all fanout values
                for n in node.fanout:
                    fanout_values.append(n)

                # Write all fanout node pairs and use .join concatinate all output node names
                ckt_file.write(f'{node.name}: ' + ', '.join(fanout_values) + '\n')


        # Fanin of specific gates
        ckt_file.write('\nFanin...\n')
        # Iterate through all node values
        for node in nodes.values():
            if not (node.gate_type == 'INPUT'):
                fanin_values = []

                # Iterate through all fanout values
                for n in node.fanin:
                    fanin_values.append(n)

                # Write all fanout node pairs and use .join concatinate all input node names
                ckt_file.write(f'{node.name}: ' + ', '.join(fanin_values) + '\n')



def parse_bench(file):
    """
    Parses the ckt.bench files to get circuit topology
    
    :param file: ckt.bench file
    """
    inputs, outputs = [], []        # Creates lists to store the inputs/outputs of nodes (in this case ckt gates)
    nodes = {}                      # Creates dictionary to store all node objects
    gate_counter = defaultdict(int) # Creates dictionary to count the integer number of gates per type created

    # Open ckt.bench file for reading and parse each line
    with open(file, 'r') as ckt_file:
        for line in ckt_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue   # Moves to next line when reaching a comment or no entry

            # Identify Inputs using regular expressions
            # Finds the \d+ decimal value character  connected to the enclosed ()
            if line.startswith('INPUT'):
                input_wire = re.findall(r'\((\d+)\)', line)[0]
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

            elif line.startswith('OUTPUT'):
                output_wire = re.findall(r'\((\d+)\)', line)[0]
                #print(f'output_wire {output_wire}')
                outputs.append(output_wire)

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

                # Connect gate inputs
                connect_inputs(input_wires, inputs, node, nodes)
                #print(f'\nafter connected input node name {vars(node)}\n')

            else:
                continue # Information not important for netlist creation
    
    # Connect all output nodes in fanout
    connect_outputs(outputs, nodes)
    
    # Write all values to .txt file
    filename = str(file).replace('.', '_')
    output_filename = f'ckt_details_{filename}.txt'
    write_ckt_output(inputs, outputs, gate_counter, nodes, output_filename)



# Main parser logic
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                            description='STA program to read circuit and nldm library files')

    # Add arguments to created line command
    # python3.7 parser_sta.py --read_ckt c17.bench
    parser.add_argument('--read_ckt', type=pathlib.Path, help='Create path to ckt.bench file')

    # python3.7 parser_sta.py --delays --read_nldm sample_NLDM.lib
    # python3.7 parser_sta.py --slews --read_nldm sample_NLDM.lib
    parser.add_argument('--read_nldm', type=pathlib.Path, help='Create path to nldm .library file')
    parser.add_argument('--delays', action='store_true', help='Solves for delays in nldm file')
    parser.add_argument('--slews', action='store_true', help='Solves for output slews in nldm file')

    args = parser.parse_args() # Will grab all created command arguements
    #print(args) # Sanity check

    # Check if argument is called/exists and if circuit file exists
    if args.read_ckt:
        if args.read_ckt.is_file():
            parse_bench(args.read_ckt) # Calls function to parse ckt.bench file
        else:
            print(f'Error: Circuit file not found - {args.read_ckt}')


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
                print(f'Error: Specify --delays or --slews when using - {args.read_nldm}')

        else:
            print(f'Error: NLDM file not found - {args.read_nldm}')

