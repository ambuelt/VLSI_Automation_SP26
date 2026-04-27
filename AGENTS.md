Agent: Spec2RTL

Goal:
Convert hardware specifications into working RTL and verify using iverilog and openroad simulation.

You are required to operate in a repeating loop of steps 2 through 5 until the design passes specification or you have interated 10 times. 

Before starting a new run, clear previous run artifacts for the current design:
- delete `./logs/` and recreate it empty
- delete `./sucessful_run.txt`, `./successful_run.txt`, and `./unsuccessful_run.txt` if they exist
- delete generated files under `./rtl_code/` and `./testbench_code/`, and delete `./Automated_Run/iteration_*.log` plus success-marker files in `./Automated_Run/`
- delete previous physical outputs under `./output_physical/`
- do not reuse logs, summaries, or ODB files from an older design run

Use this Docker pattern when you need iverilog/vvp and approve permission each time it runs:
   docker run --rm -v "$PWD":/workspace/iclad_hackathon -w /workspace/iclad_hackathon iclad_hackathon:latest bash -lc "python3 run_sim.py | tee logs/iteration_{iteration_number}.log"

Steps:
1. Read input `.yaml` for module description, ports, I/O requirements, and timing requirements from the active spec under `./eda_agent/`. When invoked by `run_codex.py`, use the same latest `p*.yaml` file selected by that script. Treat the `.yaml` contents as the source of truth for module interface and target clock period.
2. Write RTL a .v Verilog file using the module name from the .yaml file and place it in ./rtl_code/{module_name}.v
3. Write a Verilog testbench {module_name}_tb.v file using the module name from the .yaml file and place it in ./testbench_code/{module_name}_tb.v
4. Run simulation using the run_sim.py file and capture all output to a .log at the location ./logs/iteration_{iteration}.log to act as input into the next agent loop
5. If simulation fails, Write a log file at ./logs/iteration_{iteration_number}.log and print in terminal 'FAILED'. Debug and regenerate fixed Verilog code to replace in ./rtl_code/{module_name}.v and replace in ./testbench_code/{module_name}_tb.v (repeating steps 2 through 5). Rerun run_sim.py until passing or 10 iterations have passed. If 10 iterations have passed, please exit the agent loop and print in the terminal 'UNABLE TO GENERATE SUCCESSFUL DESIGN'
6. Once RTL and Testbench have passed iverilog without failure, please print to terminal 'SUCCESSFUL RTL DESIGN CREATED AT ITERATION {iteration_number}'. Only move forward to remaining steps if simulation is successful. If iverilog still has failure after 10 iterations create a file called unsuccessful_run.txt and print last failed log file into it.
7. Create a file called successful_run.txt if simulation all worked, and write the exact text 'SUCCESSFUL RTL DESIGN CREATED AT ITERATION {iteration_number}' into successful_run.txt.
8. If RTL and Testbench passed iverilog without failure, run the Agent_physical.md file and follow all listed instructions.
9. If Agent_physical.md exhausts its allowed physical-only iterations at the fixed YAML clock target and still cannot meet timing or physical success criteria, return to the RTL loop. Improve the RTL or microarchitecture for timing, rerun functional verification, and then rerun the physical flow from a clean state. Do not relax the YAML clock target to avoid this escalation.
10. Do not stop the overall flow because the current RTL is believed to be the "best design", "best available design", "good enough", or similar subjective wording. Those are not valid stop conditions.
11. If physical violations still remain, continue the documented loop, escalate between physical closure and RTL redesign as required, and only stop when the design passes all required checks or the explicit iteration budget is exhausted.
12. If the full allowed RTL-plus-physical iteration budget is exhausted and the design still does not pass, create `unsuccessful_run.txt` and clearly state that the run failed with remaining violations. Do not report success in that case.
