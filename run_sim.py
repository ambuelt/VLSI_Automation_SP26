# File taken from Canvas Agent Instructions

import subprocess

def run_sim():
    cmd = [
        "iverilog",
        "-o",
        "sim.out",
        "rtl_code/seq_detector_0011.v",
        "testbench_code/seq_detector_0011_tb.v"
    ]
    
    subprocess.run(cmd)

    result = subprocess.run(
        ["vvp", "sim.out"],
        capture_output=True
    )

    return result.stdout.decode()


# /OpenROAD-flow-scripts/tools/install/OpenROAD/bin/openroad

if __name__ == "__main__":
    print(run_sim())
