# Parser File to Read circuits

import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict

class Node:
    def __init__(self, gate_name, gate_type=None):
        """
        Docstring for __init__
        
        :param self: Description
        :param gate_name: Description
        :param gate_type: Description
        """
        self.name = gate_name
        self.type = gate_type
        self.fanin = []
        self.fanout = []

class LUT:
    def __init__(self):
        """
        Docstring for __init__
        
        :param self: Description
        :param gate_name: Description
        :param gate_type: Description
        """
        self.all_gate_names = 1

def connect_inputs(input_wires, ckt_inputs, nodes: dict) -> Node:
    """
    Docstring for connect_inputs
    
    :param input_wires: Description
    :param nodes: Description
    :type nodes: dict

    :return: Description
    :rtype: Node
    """
    for input in input_wires:
        input = input.strip()

        if input in ckt_inputs:
            input_node = nodes[f'INPUT-{input}']
        else:
            input_node = Node(input)

    return input_node


def connect_outputs(output_wires, nodes: dict):
    """
    Connects final outputs of the circuit
    
    :param output_wires: Description
    :param nodes: Description
    :type nodes: dict
    """
    
    # Checks all output_wires against the node values to determine where they are in circuit
    for output in output_wires:
        for node in nodes.values():

            # If output is only connected to a number, replace it with OUTPUT-that number
            if node.name.endswith(f'-{output}'):
                output_node = Node(f'OUTPUT-{output}', 'OUTPUT') # Creates new OUTPUT node type
                node.fanout.append(output_node)



def write_ckt_output(ckt_inputs, ckt_outputs, gate_counter, nodes, output_file='ckt_details.txt'):
    """
    Docstring for write_ckt_output
    
    :param output_file: Description
    """

    # Open output circuit file for writing line by line
    with open(output_file, 'w') as ckt_file:
        ckt_file.write(f'{len(ckt_inputs)} primary inputs')
        ckt_file.write(f'{len(ckt_outputs)} primary outputs')

        # Iterate through gate types to print all gate values per type
        for gate_type, count in gate_counter.items():
            ckt_file.write(f'{count} {gate_type} gates\n')

        # Fanout of specific gates
        ckt_file.write('Fanout...\n')
        # Iterate through all node values
        for node in nodes.values():
            fanout_values = []

            # Iterate through all fanout values
            for n in node.fanout:
                fanout_values.append(n.name)

            # Write all fanout node pairs and use .join concatinate all output node names
            ckt_file.write(f'{node.name}: {','.join(fanout_values)}\n')


        # Fanin of specific gates
        ckt_file.write('Fanin...\n')
        # Iterate through all node values
        for node in nodes.values():
            fanin_values = []

            # Iterate through all fanout values
            for n in node.fanin:
                fanin_values.append(n.name)

            # Write all fanout node pairs and use .join concatinate all input node names
            ckt_file.write(f'{node.name}: {','.join(fanin_values)}\n')



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
                inputs.append(input_wire)

                input_name = f'INPUT-{input_wire}'

                # Create INPUT nodes for starting gates
                # Checks to see if node has already been created, if not, adds it to netlist
                if gate_name not in nodes:
                    nodes[input_name] = Node(input_name, 'INPUT')
                    input_node = nodes[input_name]
                else:
                    input_node = nodes[input_name]

            elif line.startswith('OUTPUT'):
                output_wire = re.findall(r'\((\d+)\)', line)[0]
                outputs.append(output_wire)

            elif ('=') in line:
                gate_name, gate = line.split('=')
                output_wire_name = gate_name.strip()

                # Finds the \w+ word character instance connected to the initial ( ex. 'name('
                gate_type = re.findall(r'(\w+)\()', gate)[0]

                # Finds all values contained in paratheses and splits all inputs seperated by commas to get a list ['n1', 'n2', 'n3',...]
                input_wires = re.findall(r'\((.*?)\)', gate)[0].split(',')

                gate_name = f'{gate_type}-{output_wire_name}'

                # Checks to see if node has already been created, if not, adds it to netlist
                if gate_name not in nodes:
                    nodes[gate_name] = Node(gate_name, gate_type)
                    node = nodes[gate_name]
                else:
                    node = nodes[gate_name]

                # Increment the number of gates of that type by 1
                gate_counter[gate_type] = +1

                # Connect gate inputs
                input_node = connect_inputs(input_wires, inputs, nodes)

                # Add all fanin and fanouts to circuit
                node.fanin.append(input_node)
                input_node.fanout.append(node)


            else:
                continue # Information not important for netlist creation
    
    # Connect all output nodes in fanout
    connect_outputs(outputs, nodes)
    
    # Write all values to .txt file
    output_filename = 'ckt_details.txt'
    write_ckt_output(inputs, outputs, gate_counter, nodes, output_filename)


def write_nldm_output(delay_or_slew, cells, output_file='ckt_details.txt'):
    """
    Docstring for write_nldm_output
    
    :param mode: Description
    :param output_file: Description
    """

    # Open output nldm file for writing line by line
    with open(output_file, 'w') as nldm_file:
        for cell_name, cell_data in cells.items():
            nldm_file.write(f'cell: {cell_name} \n')
            
            output_time = cell_data[delay_or_slew]

            slews = ','.join(map(str, output_time['index_1']) + "\n")
            caps = ','.join(map(str, output_time['index_2']) + "\n")

            nldm_file.write(f'input slews: {slews}')
            nldm_file.write(f'load cap: {caps}')

            for row in output_time['delay_or_slew']:
                times = ','.join(map(str, row) + "; \n")
                nldm_file.write(f'{delay_or_slew}: {times}')


def parse_nldm(file, delay_or_slew):
    """
    Docstring for parse_nldm
    
    :param file: nldm .library file
    :param delay_or_slew: Determines whether the command line prompt wants to calculate delay or slew
    """

    cells = {}

    with open(file, 'r') as lib_file:
        file_txt = lib_file.read()  # Reads entire file to then edit off of


        # GRab each cell block of code from .lib file
        # re.S used to match newlines for multi-line txt
        # Gives list of tuples of (cell_name, txt inside {})
        cell_data = re.findall(r'cell\s*\( (.*?) \) \s*\{ (.*?)\n \s*\}', file_txt, re.S)

        for cell_name, data in cell_data:
            cell_values = {} # Creates dictionary to store input cap, delay, and slew values

            # Finds all values contained in paratheses and splits all inputs seperated by commas to get a list ['n1', 'n2', 'n3',...]
            c_name = re.findall(r'\((.*?)\)', cell_name)[0]

            # Grabs decimal number values and '.' for float number
            cap_value = re.search(r'capacitance \s*: \s*([\d\.]+)', data)
            delay_value = re.search(r'cell_delay.*? \{ (.*?) \}', data, re.S)
            slew_value = re.search(r'output_slew.*? \{ (.*?) \}', data, re.S)
            
            # If the capacitance text is found, add to cell_value dict
            if cap_value:
                cell_values['capacitance'] = float(cap_value.group(1)) # Use group 1 to get first instance of actual value

            # If the delay text is found, add to cell_value dict
            if delay_value:
                cell_values['delay'] = float(cap_value.group(1)) # Use group 1 to get first instance of actual value

                ## NEED TO ADD THE WAY TO FIND THE VALUES IN THE 2D ARRARY!!!!

            # If the slew text is found, add to cell_value dict
            if slew_value:
                cell_values['slew'] = float(cap_value.group(1)) # Use group 1 to get first instance of actual value

                ## NEED TO ADD THE WAY TO FIND THE VALUES IN THE 2D ARRARY!!!!

    # Write all values to .txt file
    if (delay_or_slew == 'delays'):
        output_filename = 'delay_LUT.txt'
    elif (delay_or_slew == 'slews'):
        output_filename = 'slew_LUT.txt'
    else:
        print(f'Something went wrong???')
        exit(1)
    
    write_nldm_output(delay_or_slew, cells, output_filename)




# Main parser logic
if __name__ == '__main__':
    parser = argparse.ArguementParser(
                            description='STA program to read circuit and nldm library files')

    parser.add_argument('--read_ckt', type=pathlib.Path, help='Create path to ckt.bench file')

    # Add arguments to created line command
    # python3.7 parser_sta.py -- delays -- read_nldm sample_NLDM.lib
    # python3.7 parser_sta.py -- slews -- read_nldm sample_NLDM.lib
    parser.add_argument('--read_nldm', type=pathlib.Path, help='Create path to nldm .library file')
    parser.add_argument('--delays', action='store_true', help='Solves for delays in nldm file')
    parser.add_argument('--slews', action='store_true', help='Solves for output slews in nldm file')

    args = parser.parse_args() # Will grab all created command arguements
    print(args) # Sanity check

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
                parse_nldm(args.read_nldm, args.delays) # Calls function to parse .lib file for delays
            elif args.slews:
                parse_nldm(args.read_nldm, args.slews)  # Calls function to parse .lib file for slews
            else:
                print(f'Error: Specify --delays or --slews when using - {args.read_nldm}')

        else:
            print(f'Error: NLDM file not found - {args.read_nldm}')



