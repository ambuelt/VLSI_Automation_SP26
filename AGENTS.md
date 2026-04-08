Agent: Spec2RTL

Goal:
Convert hardware specifications into working RTL and verify using iverilog and openroad simulation.

You are required to operate in a repeating loop of steps 2 through 5 until the design passes specification or you have interated 10 times. 

Use this Docker pattern when you need iverilog/vvp and approve permission each time it runs:
   docker run --rm -v "$PWD":/workspace/iclad_hackathon -w /workspace/iclad_hackathon iclad_hackathon:latest bash -lc "python3 run_sim.py | tee logs/iteration_{iteration_number}.log"

Steps:
1. Read input .yaml for module description, ports, and I/O requirements from the location ./eda_agent/p1.yaml
2. Write RTL a .v Verilog file using the module name from the .yaml file and place it in ./rtl_code/{module_name}.v
3. Write a Verilog testbench {module_name}_tb.v file using the module name from the .yaml file and place it in ./testbench_code/{module_name}_tb.v
4. Run simulation using the run_sim.py file and capture all output to a .log at the location ./logs/iteration_{iteration}.log to act as input into the next agent loop
5. If simulation fails, Write a log file at ./logs/iteration_{iteration_number}.log and print in terminal 'FAILED'. Debug and regenerate fixed Verilog code to replace in ./rtl_code/{module_name}.v and replace in ./testbench_code/{module_name}_tb.v (repeating steps 2 through 5). Rerun run_sim.py until passing or 10 iterations have passed. If 10 iterations have passed, please exit the agent loop and print in the terminal 'UNABLE TO GENERATE SUCCESSFUL DESIGN'
6. Once RTL and Testbench have passed iverilog without failure, please print to terminal 'SUCCESSFUL RTL DESIGN CREATED AT ITERATION {iteration_number}'. Only move forward to remaining steps if simulation is successful.
7. Create a file called sucessful_run.txt if simulation all worked. 
