################################################################################
# Assignment : Mini-Project 1 - Phase 1                                        #
# Team: Ctrl Freaks                                                            #
# ---------------------------------------------------------------------------  #
#                                                                              #
# LUT class to generate the netlist and get gate info into txt files           #
################################################################################

# All automatically in python 3.7 terminal except for numpy and pathlib
import argparse
import pathlib
import numpy as np
import re
from collections import defaultdict
from collections import deque

class LUT:
    def __init__(self):
        """
        Creates a class LUT to represent the different cells in the nldm library file
        
        :param self: Used to call local variables of class LUT
        """
        self.full_cell = {}             # Dictionary to store all cells based on name with a nested dictionary to hold all the values
                                        # This dictionary contains all the following information in it every time for ease of calling

        # All of these are instead replaced by the dictionary keys = cell_name with the values for each key. 
        # This made it easier to call for certain cells rather than rely on numbers
        self.Allgate_name = []          # all cells defined in the LUT  <- acts as keys in dictionary
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
        
        # ex. cell: INVx1
        # cap:     capacitance             : 1.700230
        # data: cell_delay(Timing_7_7) {...}
        # data: index_1(...); index_2(...); values(2D array)   <- for output_slew
        for cell, cap, delay, slew in cell_body:
            cell_values = {}              # dictionary to store all future array values

            # ([\d\.]+) - captures all digit values including the decimal for the decimal number assuming there is at least 1 number
            # [0] - grabs the value from the list instead of just returning a list with the value in it
            cap_value = re.findall(r'capacitance\s*:\s*([\d\.]+)', cap)[0]
            cell_capacitance = float(cap_value)

            # Extract cell delay values (index 1 and 2 are to be the same regardless of delay or slew)
            index_1 = re.findall(r'index_1\s*\("(.*?)"\)', delay)[0]
            index_2 = re.findall(r'index_2\s*\("(.*?)"\)', delay)[0]
            delay_values = re.findall(r'values\s*\((.*?)\);', delay, re.S)[0] # Has the entire list and will need to parse for valures
            slew_values = re.findall(r'values\s*\((.*?)\);', slew, re.S)[0]   # Has the entire list and will need to parse for valures

            # Create 1D arrays of size 7 to store different tau and load_cap values
            tau_values = np.zeros(7)
            load_cap_values = np.zeros(7)

            # Use to track integer position in np.array to add slew values to specific 1D array index
            index = 0
            for tau in index_1.split(','):
                tau_values[index] = float(tau)
                index += 1

            # Redo process for index_2
            index = 0
            for load_cap in index_2.split(','):
                load_cap_values[index] = float(load_cap)
                index += 1

            # Parse delay and slew and get rid of all tab, newline, and \ characters that would complicate parsing
            delay_time = delay_values.replace('\\', '').replace('\n','').replace('\t','')
            slew_time = slew_values.replace('\\', '').replace('\n','').replace('\t','')

            # Put row by row into a list format to access each as needed
            delay_rows = re.findall(r'"(.*?)"', delay_time, re.S)
            slew_rows = re.findall(r'"(.*?)"', slew_time, re.S)

            # Set size of array to 7 by 7 as per project instructions
            delay_array = np.zeros((7,7)) # Make 2D arrary for delay
            slew_array = np.zeros((7,7)) # Make 2D arrary for slew
            
            # Use to track integer position in np.array to add slew values to specific 2D array index
            array_position_row = 0
            array_position_col = 0

            # Run through delay values in each row and split into columns using commas
            for row in delay_rows:
                for col in row.split(','):
                    delay_array[array_position_row][array_position_col] = float(col)
                    array_position_col += 1

                array_position_row += 1  # Move to next row
                array_position_col = 0   # Reset columns to not go out of index

            # Use to track integer position in np.array to add slew values to specific 2D array index
            array_position_row = 0
            array_position_col = 0

            # Run through slew values in each row and split into columns using commas
            for row in slew_rows:
                for col in row.split(','):
                    slew_array[array_position_row][array_position_col] = float(col)
                    array_position_col += 1

                array_position_row += 1  # Move to next row
                array_position_col = 0   # Reset columns to not go out of index

            # Creates dictionary to store input cap, delay, and slew values
            cell_values = {
                'input_cap': cell_capacitance,
                'index_1': tau_values,
                'index_2': load_cap_values,
                'delays': delay_array,
                'slews': slew_array
            }

            self.full_cell[cell] = cell_values   # Create a dictionary within a dictionary to use the cell names to call values!!


        # Write all values to .txt file
        if (delay_or_slew == 'delays'):
            output_filename = 'delay_LUT.txt'
            self.write_nldm_output(delay_or_slew, output_filename)   # Write to .txt with assignment format

        elif (delay_or_slew == 'slews'):
            output_filename = 'slew_LUT.txt'
            self.write_nldm_output(delay_or_slew, output_filename)   # Write to .txt with assignment format

