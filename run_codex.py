# File taken from Canvas Agent Instructions

import re
import shutil
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EDA_DIR = ROOT / "eda_agent"
LOGS_DIR = ROOT / "logs"
OUTPUT_PHYSICAL_DIR = ROOT / "output_physical"


def discover_spec_file() -> Path:
    specs = list(EDA_DIR.glob("p*.yaml"))
    if not specs:
        raise FileNotFoundError("No spec files found under eda_agent/")

    def sort_key(path: Path):
        match = re.fullmatch(r"p(\d+)\.yaml", path.name)
        return (int(match.group(1)) if match else -1, path.stat().st_mtime_ns)

    return max(specs, key=sort_key)


def discover_module_name(spec_path: Path) -> str:
    for line in spec_path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", stripped)
        if match:
            return match.group(1)
    raise ValueError(f"Unable to determine module name from {spec_path}")


def clean_previous_run(module_name: str) -> None:
    if LOGS_DIR.exists():
        shutil.rmtree(LOGS_DIR)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    module_output_dir = OUTPUT_PHYSICAL_DIR / module_name
    if module_output_dir.exists():
        shutil.rmtree(module_output_dir)

    # Clean legacy flat physical output too, because older agents wrote here.
    if OUTPUT_PHYSICAL_DIR.exists():
        for child in list(OUTPUT_PHYSICAL_DIR.iterdir()):
            if child.is_dir() and child.name != module_name:
                shutil.rmtree(child)
            elif child.is_file():
                child.unlink()

    for stale_file in [
        ROOT / "sucessful_run.txt",
        ROOT / "successful_run.txt",
        ROOT / "unsuccessful_run.txt",
        ROOT / "sim.out",
    ]:
        if stale_file.exists():
            stale_file.unlink()


def run_codex():
    spec_path = discover_spec_file()
    module_name = discover_module_name(spec_path)
    clean_previous_run(module_name)
    start_time = time.time()

    prompt = """
    Read the AGENTS.md file and follow all listed instructions.
    """

    cmd = [
        "codex",
        "exec",
        "--skip-git-repo-check",
        "--cd",
        str(ROOT),
        "--dangerously-bypass-approvals-and-sandbox",
        prompt,
    ]

    result = subprocess.run(cmd, text=True, capture_output=True)
    elapsed_time = time.time() - start_time

    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    print(f"run_codex runtime: {elapsed_time:.2f} seconds")

    return result.returncode


if __name__ == "__main__":
    raise SystemExit(run_codex())
