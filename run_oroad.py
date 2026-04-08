# File taken from Canvas Agent Instructions

import subprocess

def run_oroad():
    cmd = [
        "iverilog",
        "-o",
        "my_sim.out",
        "rtl/design.v",
        "tb/iclad_seq_detector_tb.v"
    ]
    
    subprocess.run(cmd)

    result = subprocess.run(
        ["vvp", "my_sim.out"],
        capture_output=True
    )

    return result.stdout.decode()


if __name__ == "__main__":
    print(run_oroad())