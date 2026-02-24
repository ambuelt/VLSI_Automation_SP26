# VLSI_Automation_SP26 - Mini Project 1 README
Repository to hold mini project 1 for EEE598 - VLSI Automation class

This mini-project 1 will parse the test benches and nldm library files (phase 1) and 
calculate the delay and slew from traversing through the circuit (phase 2).

<br>

**Instructions for Running Python Code** - *Setting up virtual env and packages*

python3.7 -m venv <name of venv>

source <name of venv>/bin/activate

pip3 install -r requirements.txt

python3.7 parser.py --read_ckt c17.bench

python3.7 parser.py --read_ckt c7552.bench

python3.7 parser.py --read_ckt b15.bench

python3.7 parser.py --delays --read_nldm sample_NLDM.lib

python3.7 parser.py --slews --read_nldm sample_NLDM.lib

<br>

**All Files + Folders and their description**

|Filename:                  |                 Description:  |
|           :---            |              :---             |
|parser.py                  |                 - Acts as the main python file with Node and LUT classes to parse and print the different .txt outputs |
|requirements.txt           |                 - Includes all python packages to install for code (some packages used should automatically be built into python 3.7) |
|b15.bench                  |                 - Largest circuit test bench |
|c17.bench                  |                 - Smallest circuit test bench |
|c7552.bench                |                 - Mid-size circuit test bench |
|sample_NLDM.lib            |                 - Library file holding the different types of cells and their delay, cap, and slew values |
  
<br>

*All of the following is not needed for running this assignment*

|Filename:                         |         Description:  |
|           :---                   |           :---        |
|.gitignore                        |        - automatically generated when making the repository |
|Classes_Nodes_LUT                 |        - Was the prelimary file to store the node and lut classes based on the assignment desciption before moved to parser.py |
|EECAD Remote Access Instructions  |        - Given in assignment files to test code on eecad machines |
|ProjectDescription                |        - Given in assignment files to provide mini project 1 instructions |
|Rubrics                           |        - Given in assignment files to show how grading will be done |
