import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EDA_DIR = ROOT / "eda_agent"
RTL_DIR = ROOT / "rtl_code"
TB_DIR = ROOT / "testbench_code"


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


def run_sim() -> str:
    spec_path = discover_spec_file()
    module_name = discover_module_name(spec_path)
    rtl_path = RTL_DIR / f"{module_name}.v"
    tb_path = TB_DIR / f"{module_name}_tb.v"

    if not rtl_path.exists():
        return f"Missing RTL file: {rtl_path}\n"
    if not tb_path.exists():
        return f"Missing testbench file: {tb_path}\n"

    compile_cmd = [
        "iverilog",
        "-g2012",
        "-o",
        "sim.out",
        str(rtl_path),
        str(tb_path),
    ]

    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    if compile_result.returncode != 0:
        return compile_result.stdout + compile_result.stderr

    result = subprocess.run(["vvp", "sim.out"], capture_output=True, text=True)
    return result.stdout + result.stderr


if __name__ == "__main__":
    print(run_sim(), end="")
