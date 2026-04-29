import re
import shutil
import subprocess
import time
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EDA_DIR = ROOT / "eda_agent"
LOGS_DIR = ROOT / "logs"
OUTPUT_PHYSICAL_DIR = ROOT / "output_physical"
RESULTS_DIR = ROOT / "results"


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


def summarize_json_metrics(module_name: str) -> str:
    # Provide a compact metric snapshot to the next Codex continuation pass
    # so it can resume from the current physical state instead of restarting.
    physical_logs = OUTPUT_PHYSICAL_DIR / module_name / "logs"
    report_json = physical_logs / "6_report.json"
    route_json = physical_logs / "5_2_route.json"
    if not report_json.exists():
        return "Final report JSON is missing"

    report = json.loads(report_json.read_text())
    parts = [
        f"final setup TNS={report.get('finish__timing__setup__tns', 'missing')}",
        f"final hold TNS={report.get('finish__timing__hold__tns', 'missing')}",
        f"final setup WNS={report.get('finish__timing__setup__ws', 'missing')}",
        f"final hold WNS={report.get('finish__timing__hold__ws', 'missing')}",
        f"final setup violations={report.get('finish__timing__drv__setup_violation_count', 'missing')}",
        f"final hold violations={report.get('finish__timing__drv__hold_violation_count', 'missing')}",
        f"final flow errors={report.get('finish__flow__errors__count', 'missing')}",
    ]
    if route_json.exists():
        route = json.loads(route_json.read_text())
        parts.append(
            f"route DRC={route.get('detailedroute__route__drc_errors', 'missing')}"
        )
    return ", ".join(parts)


def get_run_state(module_name: str) -> tuple[str, list[str]]:
    # This runner acts as a supervisor: it does not trust a single Codex pass
    # to stop at the right time, so it validates the required AGENTS /
    # Agent_physical outputs before declaring success.
    reasons: list[str] = []

    unsuccessful = ROOT / "unsuccessful_run.txt"
    if unsuccessful.exists():
        return "failed", [f"{unsuccessful.name} exists"]

    success_marker = ROOT / "successful_run.txt"
    if not success_marker.exists():
        reasons.append("successful_run.txt is missing")

    physical_dir = OUTPUT_PHYSICAL_DIR / module_name
    evaluation_summary = physical_dir / f"{module_name}_evaluation_summary.md"
    iteration_summaries = list(physical_dir.glob(f"iteration_*_{module_name}_summary.md"))
    final_gds = physical_dir / f"{module_name}.gds"
    flat_odb = RESULTS_DIR / f"{module_name}.odb"
    flat_gds = RESULTS_DIR / f"{module_name}.gds"
    flat_sdc = RESULTS_DIR / f"{module_name}.sdc"
    report_json = physical_dir / "logs" / "6_report.json"
    route_json = physical_dir / "logs" / "5_2_route.json"

    if not physical_dir.exists():
        reasons.append(f"{physical_dir} is missing")
        return "incomplete", reasons

    if not report_json.exists():
        reasons.append("final 6_report.json is missing")
    if not route_json.exists():
        reasons.append("final 5_2_route.json is missing")
    if not final_gds.exists():
        reasons.append("final GDS is missing")
    if not flat_odb.exists():
        reasons.append("flat final ODB is missing")
    if not flat_gds.exists():
        reasons.append("flat final GDS is missing")
    if not flat_sdc.exists():
        reasons.append("flat final SDC is missing")
    if not iteration_summaries:
        reasons.append("iteration summary markdown is missing")
    if not evaluation_summary.exists():
        reasons.append("evaluation summary markdown is missing")

    if reasons:
        return "incomplete", reasons

    report = json.loads(report_json.read_text())
    route = json.loads(route_json.read_text())

    if report.get("finish__timing__setup__tns") != 0:
        reasons.append("final setup TNS is nonzero")
    if report.get("finish__timing__hold__tns") != 0:
        reasons.append("final hold TNS is nonzero")
    if report.get("finish__timing__drv__setup_violation_count") != 0:
        reasons.append("final setup violation count is nonzero")
    if report.get("finish__timing__drv__hold_violation_count") != 0:
        reasons.append("final hold violation count is nonzero")
    if report.get("finish__flow__errors__count") != 0:
        reasons.append("final flow error count is nonzero")
    if route.get("detailedroute__route__drc_errors") != 0:
        reasons.append("final routed DRC is nonzero")

    if reasons:
        return "incomplete", reasons
    return "success", []


def run_codex() -> int:
    spec_path = discover_spec_file()
    module_name = discover_module_name(spec_path)
    clean_previous_run(module_name)
    start_time = time.time()

    prompts = [
        "Read the AGENTS.md file and follow all listed instructions. "
        "Use the active YAML spec under eda_agent/."
    ]
    attempt = 0

    while True:
        attempt += 1
        # Launch one Codex pass. If it stops early, we inspect the workspace
        # and decide whether to continue from the current state.
        cmd = [
            "codex",
            "exec",
            "--skip-git-repo-check",
            "--cd",
            str(ROOT),
            "--dangerously-bypass-approvals-and-sandbox",
            prompts[-1],
        ]

        result = subprocess.run(cmd, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)

        state, reasons = get_run_state(module_name)
        if state == "success":
            elapsed_time = time.time() - start_time
            print(f"run_codex runtime: {elapsed_time:.2f} seconds")
            return 0

        if state == "failed":
            elapsed_time = time.time() - start_time
            print("Run failed:")
            for reason in reasons:
                print(f"- {reason}")
            print(f"run_codex runtime: {elapsed_time:.2f} seconds")
            return 1

        # Continue from existing artifacts instead of wiping the run and
        # starting from scratch. This mirrors the manual terminal workflow,
        # where the controller keeps moving the same run forward.
        continuation_prompt = (
            f"Continue the existing AGENTS.md run for {spec_path.name} and module {module_name}. "
            "Do not restart from scratch and do not delete current artifacts. "
            "Use the current workspace state, including generated RTL, logs, OpenROAD outputs, and partial summaries. "
            "Only perform the missing next steps required to complete the run. "
            "Current issues: "
            + "; ".join(reasons)
            + ". Current metrics summary: "
            + summarize_json_metrics(module_name)
            + ". Finish only when AGENTS.md and Agent_physical.md completion conditions are actually satisfied."
        )
        prompts.append(continuation_prompt)

        # Safety cap for runner supervision only. The design-loop policy itself
        # still lives in AGENTS.md / Agent_physical.md.
        if attempt >= 6:
            elapsed_time = time.time() - start_time
            print("Run remained incomplete after continuation attempts:")
            for reason in reasons:
                print(f"- {reason}")
            print(f"run_codex runtime: {elapsed_time:.2f} seconds")
            return 1


if __name__ == "__main__":
    raise SystemExit(run_codex())
