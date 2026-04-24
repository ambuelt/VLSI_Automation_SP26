# File taken from Canvas Agent Instructions

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def run_codex():
    # Add prompt to give to Codex AGENTS.md initial prompting
    prompt = f"""
    Read the AGENTS_physical.md file and follow all listed instructions.
    """

    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--cd",
        str(ROOT),
        "--dangerously-bypass-approvals-and-sandbox",
        prompt
    ]
    
    result = subprocess.run(cmd,
                   text=True,
                   capture_output=True)
    
    print(result.stdout)
    if result.stderr:
        print(result.stderr)



if __name__ == "__main__":
    raise SystemExit(run_codex())
    



if __name__ == "__main__":
    print(run_oroad())