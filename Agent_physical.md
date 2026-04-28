# Physical Closure Agent (OpenROAD)

## Objective
Perform physical design evaluation and limited physical-closure repair on RTL generated from `AGENTS.md` using the OpenROAD flow.

Store retained artifacts in a module-specific folder:
- `output_physical/{module_name}/`

Do not reuse flat generic retained filenames across different designs.

---

## Inputs
- RTL file generated from the functional agent flow
- top module name
- active YAML spec used for the run, including its `clock_period`
- `successful_run.txt` indicating RTL passed simulation

---

## Required Behavior

Run in an iterative loop until one of the following is true:
- post-CTS and routing-stage timing and physical checks meet the targeted criteria
- 5 physical iterations have been completed

For each iteration:
1. generate or update constraints and ORFS config for `{module_name}`
2. run OpenROAD in Docker
3. copy logs, reports, and result databases back into `output_physical/{module_name}/`
4. inspect violations and QoR
5. if violations remain, adjust constraints or config and rerun

If the targeted checks pass, stop and report success.
If 5 iterations are exhausted, stop the physical-only loop, report the best available result plus remaining violations, and escalate back to the RTL agent for microarchitectural redesign at the same YAML clock target.

Mandatory loop rule:
- if any targeted violation remains after an iteration, the agent must not stop at that iteration
- instead, it must either begin the next physical iteration immediately with a bounded physical fix, or explicitly escalate back to RTL redesign as soon as the physical evidence shows the current RTL is the limiting factor
- writing an iteration summary for a failing iteration is not a stop condition by itself
- completion of OpenROAD, routing, GDS generation, or summary writing does not count as success while targeted violations remain
- the agent must not stop because it believes the current RTL is the "best design", "best available design", "good enough", or because a further improvement seems unlikely
- if violations remain, the only valid outcomes are another physical iteration, escalation back to RTL redesign, or explicit failure after the documented iteration budget is exhausted

Early RTL-escalation rule:
- do not wait for all 5 physical iterations if the current data already shows the design is microarchitecturally too slow for the fixed YAML clock target
- escalate back to RTL redesign immediately once the failing behavior is clearly architectural rather than a tunable physical issue

---

## Targeted Checks

At minimum, check these metrics from post-CTS and routing-stage outputs:
- TNS
- WNS / worst slack
- setup violation count
- hold violation count
- detailed placement violations
- max slew / max capacitance violations if reported
- congestion overflow if reported
- routed DRC violations if reported
- CTS status and clock-tree QoR if reported

Success criteria:
- `tns max = 0`
- setup violation count = `0`
- hold violation count = `0`
- detailed placement violations = `0`
- no reported congestion overflow at the placement stage
- CTS must complete successfully
- routing must complete successfully
- routed DRC violations = `0` if the report is available

---

## Steps

### 1. Validate RTL
Ensure RTL passed iVerilog simulation.
- This is indicated by the existence of `successful_run.txt`

---

### 2. Create output folders

Ensure these directories exist:
- `output_physical/{module_name}/rtl/`
- `output_physical/{module_name}/sdc/`
- `output_physical/{module_name}/logs/`
- `output_physical/{module_name}/reports/`
- `output_physical/{module_name}/results/`
- `output_physical/{module_name}/odb/`
- `output_physical/{module_name}/openroad/designs/sky130hd/{module_name}/`

---

### 3. Generate or update SDC constraints

Create the constraint file at:
- `output_physical/{module_name}/sdc/{module_name}.sdc`

For sequential designs with a real clock port, derive the clock period directly from the active YAML spec and keep it identical to the spec value. Do not relax, round up, or otherwise weaken the YAML timing target between iterations.

Base template:

```tcl
create_clock -name clk -period {yaml_clock_period_ns} [get_ports clk]
set_input_delay 1 -clock clk [all_inputs]
set_output_delay 1 -clock clk [all_outputs]
```

Allowed fixes between iterations:
- refine input or output delays if the spec supports it
- keep all changes logged in the iteration summary

Prohibited fixes:
- do not change the `create_clock` period away from the YAML `clock_period`
- do not weaken timing constraints to make timing pass artificially

---

### 4. Prepare OpenROAD design config

Copy RTL into:
- `output_physical/{module_name}/rtl/{module_name}.v`

Create:
- `output_physical/{module_name}/openroad/designs/sky130hd/{module_name}/config.mk`

The config must include:
- `DESIGN_NAME`
- `PLATFORM`
- `VERILOG_FILES`
- `SDC_FILE`
- `CLOCK_PERIOD`
- `CORE_UTILIZATION`
- `PLACE_DENSITY_LB_ADDON`
- `SYNTH_REPEATABLE_BUILD`
- `LEC_CHECK = 0`

Example:

```make
export DESIGN_NAME = {module_name}
export PLATFORM = sky130hd

export VERILOG_FILES = $(abspath /OpenROAD-flow-scripts/flow/designs/src/{module_name}/{module_name}.v)
export SDC_FILE = $(abspath /OpenROAD-flow-scripts/flow/designs/src/{module_name}/{module_name}.sdc)
export CLOCK_PERIOD = {yaml_clock_period_ns}
export CORE_UTILIZATION = 55
export PLACE_DENSITY_LB_ADDON = 0.20
export SYNTH_REPEATABLE_BUILD = 1
export LEC_CHECK = 0
```

Allowed fixes between iterations:
- reduce `CORE_UTILIZATION` if congestion or placement pressure is high
- reduce `CORE_UTILIZATION` if PDN generation fails with errors such as `PDN-0185`
- adjust `PLACE_DENSITY_LB_ADDON` if global placement is too dense

Constraint rule:
- `CLOCK_PERIOD` in `config.mk` must match the active YAML `clock_period` exactly for the entire run
- if timing fails at that clock period, the iteration fails and the agent must try another physical iteration without weakening the clock target

RTL escalation rule:
- do not change the RTL during the bounded physical-only iterations
- if all allowed physical iterations are exhausted and the design still fails timing at the fixed YAML clock, hand control back to the RTL agent to improve the design and restart the flow
- if earlier physical evidence already makes it clear that bounded physical tuning is not the right lever, hand control back to the RTL agent before the 5-iteration limit

---

### 5. Stage files into ORFS

Before running ORFS inside Docker, ensure the module-specific ORFS source and config directories exist in the container:
- `/OpenROAD-flow-scripts/flow/designs/src/{module_name}/`
- `/OpenROAD-flow-scripts/flow/designs/sky130hd/{module_name}/`

Copy these files into the container paths before invoking `make`:
- `/workspace/output_physical/{module_name}/rtl/{module_name}.v`
- `/workspace/output_physical/{module_name}/sdc/{module_name}.sdc`
- `/workspace/output_physical/{module_name}/openroad/designs/sky130hd/{module_name}/config.mk`

---

### 6. Run OpenROAD using Docker

Use a Docker command that stages inputs into ORFS, runs the flow through CTS and routing, and copies artifacts back into the repo before container exit.

```bash
docker run --rm \
  -v "$PWD":/workspace \
  openroad/orfs bash -lc "
    mkdir -p /OpenROAD-flow-scripts/flow/designs/src/{module_name} \
             /OpenROAD-flow-scripts/flow/designs/sky130hd/{module_name} &&
    cp /workspace/output_physical/{module_name}/rtl/{module_name}.v \
       /OpenROAD-flow-scripts/flow/designs/src/{module_name}/{module_name}.v &&
    cp /workspace/output_physical/{module_name}/sdc/{module_name}.sdc \
       /OpenROAD-flow-scripts/flow/designs/src/{module_name}/{module_name}.sdc &&
    cp /workspace/output_physical/{module_name}/openroad/designs/sky130hd/{module_name}/config.mk \
       /OpenROAD-flow-scripts/flow/designs/sky130hd/{module_name}/config.mk &&
    cd /OpenROAD-flow-scripts/flow &&
    make DESIGN_CONFIG=designs/sky130hd/{module_name}/config.mk || true &&
    mkdir -p /workspace/output_physical/{module_name}/odb \
             /workspace/output_physical/{module_name}/logs \
             /workspace/output_physical/{module_name}/reports \
             /workspace/output_physical/{module_name}/results &&
    if [ -d /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base ]; then
      cp -r /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/* \
            /workspace/output_physical/{module_name}/results/;
    fi &&
    if [ -d /OpenROAD-flow-scripts/flow/logs/sky130hd/{module_name}/base ]; then
      cp -r /OpenROAD-flow-scripts/flow/logs/sky130hd/{module_name}/base/* \
            /workspace/output_physical/{module_name}/logs/;
    fi &&
    if [ -d /OpenROAD-flow-scripts/flow/reports/sky130hd/{module_name}/base ]; then
      cp -r /OpenROAD-flow-scripts/flow/reports/sky130hd/{module_name}/base/* \
            /workspace/output_physical/{module_name}/reports/;
    fi &&
    if [ -f /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/3_place.odb ]; then
      cp /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/3_place.odb \
         /workspace/output_physical/{module_name}/odb/{module_name}_3_place.odb;
    fi &&
    if [ -f /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/4_cts.odb ]; then
      cp /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/4_cts.odb \
         /workspace/output_physical/{module_name}/odb/{module_name}_4_cts.odb;
    fi &&
    if [ -f /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/5_route.odb ]; then
      cp /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/5_route.odb \
         /workspace/output_physical/{module_name}/odb/{module_name}_5_route.odb;
    fi &&
    if [ -f /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/6_final.gds ]; then
      cp /OpenROAD-flow-scripts/flow/results/sky130hd/{module_name}/base/6_final.gds \
         /workspace/output_physical/{module_name}/{module_name}.gds;
    fi
  "
```

This is the working module-specific command pattern used in a successful `sky130hd` run.
Do not use a hardcoded module name such as `dot_product` or a flat placeholder such as `my_design` in any copy path.

---

### 7. Copy artifacts back into the workspace

After the ORFS run, copy back all available module-specific outputs before the container exits:
- `results/sky130hd/{module_name}/base/*` into `output_physical/{module_name}/results/`
- `logs/sky130hd/{module_name}/base/*` into `output_physical/{module_name}/logs/`
- `reports/sky130hd/{module_name}/base/*` into `output_physical/{module_name}/reports/`
- `3_place.odb`, `4_cts.odb`, and `5_route.odb` into `output_physical/{module_name}/odb/`
- `6_final.gds` into the flat retained path `output_physical/{module_name}/{module_name}.gds`
- `6_final.odb`, `6_final.gds`, and `6_final.sdc` into a top-level flat folder at `results/` using module-specific names:
  - `results/{module_name}.odb`
  - `results/{module_name}.gds`
  - `results/{module_name}.sdc`

Use guarded `if [ -d ... ]` or `if [ -f ... ]` checks when copying back artifacts so failed iterations still preserve whatever partial results were produced.

---

### 8. Parse results and violations

After each iteration, inspect:
- `output_physical/{module_name}/logs/*.json`
- `output_physical/{module_name}/logs/*.log`
- `output_physical/{module_name}/reports/*.rpt`

Extract:
- area
- utilization
- power
- TNS
- WNS / worst slack
- fmax if reported
- setup and hold violation counts
- detailed placement violation count
- congestion overflow
- CTS status and failure information if present
- routed DRC count if present
- route-stage timing summary if present

Write a summary for each iteration to:
- `output_physical/{module_name}/iteration_<n>_{module_name}_summary.md`

Completion requirement:
- after each physical iteration finishes and artifacts have been copied back, the agent must write the iteration summary markdown file before considering that iteration complete
- after the final success or physical-loop exhaustion decision, the agent must also write `output_physical/{module_name}/{module_name}_evaluation_summary.md` before exiting the physical flow
- a physical run is not complete if the retained artifacts exist but these required summary markdown files are missing

---

### 9. Apply bounded fixes

If violations remain, modify only physical-flow inputs and rerun.

Continuation rule:
- after applying a bounded fix, immediately rerun the next physical iteration within the same overall flow
- do not stop after reporting a failing intermediate iteration
- do not exit the physical agent while violations remain unless the physical iteration budget has been exhausted and the agent is explicitly escalating back to RTL redesign

Preferred fix order:
1. if floorplan setup fails, add missing ORFS config fields such as `CORE_UTILIZATION`
2. if PDN generation fails with errors such as `PDN-0185`, lower `CORE_UTILIZATION` and rerun
3. if congestion is high, lower `CORE_UTILIZATION`
4. if placement density is too aggressive, tune `PLACE_DENSITY_LB_ADDON`
5. if CTS buffering or skew is problematic, adjust non-clock physical parameters conservatively and rerun
6. if routing violations or DRC remain, reduce utilization or tune other non-clock physical parameters conservatively
7. if constraints are clearly malformed, repair the SDC

Escalate to RTL redesign immediately instead of spending more physical-only iterations when one or more of these conditions is true:
1. post-CTS timing is still strongly negative after repair, for example WNS is materially negative or setup TNS remains clearly nonzero after CTS repair
2. route-stage timing repair requires large additional resizing or buffering and still leaves setup violations
3. detailed route DRC count grows large during optimization, indicating the design is fighting both timing and routability at once
4. physical tuning has already corrected congestion and legalization issues, but timing still misses because the logic depth is too high
5. the current iteration shows only marginal improvement versus the prior failing iteration while preserving the same architectural critical path

When early RTL escalation is chosen:
- stop the current physical-only line of attack
- write the iteration summary explaining why physical tuning is no longer the right lever
- return to RTL redesign immediately at the same YAML clock target
- after RTL redesign, rerun functional verification and then restart the physical flow from a clean state

Do not:
- hide violations by deleting reports
- change the YAML clock target in SDC or `config.mk`
- ignore negative timing without documenting it
- claim success if the targeted checks are not met

---

### 10. Determine stop condition

Stop with success if:
- post-CTS and route-stage reports show zero targeted violations
- `output_physical/{module_name}/odb/{module_name}_4_cts.odb` exists
- `output_physical/{module_name}/odb/{module_name}_5_route.odb` exists

Stop the physical-only loop with escalation if:
- 5 iterations are reached and violations remain
- or earlier physical evidence has already triggered the early RTL-escalation rule

Do not stop for any other reason while violations remain.
Do not stop because the design is judged subjectively as the "best design" or because a later improvement attempt looks unlikely.

On success or physical-loop exhaustion, write:
- `output_physical/{module_name}/{module_name}_evaluation_summary.md`

The summary must include:
- final area
- final power
- final slack
- remaining violations, if any
- path to the retained CTS and routed `.odb` files
- path to the retained final `.gds` file
- iteration count used
- whether RTL redesign escalation is required

If physical-loop exhaustion occurs:
- explicitly state that the design did not meet the fixed YAML clock target with physical-only fixes
- instruct the top-level agent to return to RTL generation, preserve the same YAML clock target, and rerun functional plus physical verification from a clean state
- do not claim success for the current run

---

## Notes

- Use post-CTS and route-stage outputs as the main evaluation point.
- Do not bypass CTS. The flow must actually perform clock tree synthesis and routing before claiming success.
- Use module-specific filenames in retained workspace artifacts.
- The active YAML `clock_period` is fixed for the run and must remain unchanged in both SDC and ORFS config.
- Physical-only closure is not the final fallback. If bounded physical iterations fail at the fixed YAML clock, the correct next step is RTL or microarchitecture redesign rather than clock relaxation.
- Any config or SDC change made to fix violations must be documented in the per-iteration summary.

---

## Output

- retained placement `.odb` file at `output_physical/{module_name}/odb/{module_name}_3_place.odb`
- retained CTS `.odb` file at `output_physical/{module_name}/odb/{module_name}_4_cts.odb`
- retained routed `.odb` file at `output_physical/{module_name}/odb/{module_name}_5_route.odb`
- retained final `.gds` file at `output_physical/{module_name}/{module_name}.gds`
- flat final `.odb`, `.gds`, and `.sdc` copies at `results/{module_name}.odb`, `results/{module_name}.gds`, and `results/{module_name}.sdc`
- logs in `output_physical/{module_name}/logs/`
- reports in `output_physical/{module_name}/reports/`
- SDC file at `output_physical/{module_name}/sdc/{module_name}.sdc`
- per-iteration summaries
- final evaluation summary
