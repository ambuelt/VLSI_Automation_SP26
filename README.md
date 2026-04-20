# VLSI_Automation_SP26 - Mini Project 1 README
Repository to hold mini project 1 for EEE598 - VLSI Automation class

Team: Ctrl Freaks (Annika Buelt and Shreya Tripathi)

This mini-project 1 will parse the test benches and nldm library files (phase 1) and 
calculate the delay and slew from traversing through the circuit (phase 2).

<br>

**Instructions for Running Python Code** - *Setting up virtual env and packages*

```
cd main_code

python3 -m venv .myenv

source .myenv/bin/activate

pip3 install -r requirements.txt

python3 main_parser.py --read_ckt c17.bench

python3 main_parser.py --read_ckt c7552.bench

python3 main_parser.py --read_ckt b15.bench

python3 main_parser.py --delays --read_nldm sample_NLDM.lib

python3 main_parser.py --slews --read_nldm sample_NLDM.lib

python3 main_parser.py --read_ckt c17.bench --read_nldm sample_NLDM.lib

python3 main_parser.py --read_ckt c7552.bench --read_nldm sample_NLDM.lib

python3 main_parser.py --read_ckt b15.bench --read_nldm sample_NLDM.lib
```

<br>

**All Files needed for running the code and their description (ALL LOCATED IN main_code folder)**
*Make sure to move into the main_code folder to run the code as specified as the first command in the "Instructions for Running Code" section*
|Filename:                  |                 Description:  |
|           :---            |              :---             |
|main_parser.py             |                - Acts as the main python file that calls Node and LUT classes to parse and print the different .txt outputs |
|LUT.py                     |                - Create a class LUT to represent the different cells in the nldm library file |
|Node.py                    |                - Creates a class NODE to represent the different gates in the circuit |
|requirements.txt           |                - Includes all python packages to install for code (some packages used should automatically be built into python 3.7) |
|c17.bench                  |                - Smallest circuit test bench |
|c7552.bench                |                - Mid circuit test bench      |
|b15.bench                  |                - Largest circuit test bench  |
|sample_NLDM.lib            |                - Library file holding the different types of cells and their delay, cap, and slew values |
  
<br>

*All of the following is not needed for running this assignment in terminal*
|Foldername:                       |         Description:  |
|           :---                   |           :---        |
|old_code folder                   |        - Stores the file that runs the old code submission for this Project               |
|code_outputs folder               |        - Stores the files generated from code output as run on our end since there seemed to be differences between the graders and our outputs when running our old code file *(critical paths were generated differently for b15 for some reason)*              |

|Filename:                         |         Description:  |
|           :---                   |           :---        |
|.gitignore                        |        - Automatically generated when making the repository               |
|EECAD Remote Access Instructions  |        - Given in assignment files to test code on eecad machines         |
|ProjectDescription                |        - Given in assignment files to provide mini project 1 instructions |
|Rubrics                           |        - Given in assignment files to show how grading will be done       |
