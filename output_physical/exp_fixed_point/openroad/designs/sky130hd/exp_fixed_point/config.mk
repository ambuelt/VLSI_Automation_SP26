export DESIGN_NAME = exp_fixed_point
export PLATFORM = sky130hd

export VERILOG_FILES = $(abspath /OpenROAD-flow-scripts/flow/designs/src/exp_fixed_point/exp_fixed_point.v)
export SDC_FILE = $(abspath /OpenROAD-flow-scripts/flow/designs/src/exp_fixed_point/exp_fixed_point.sdc)
export CLOCK_PERIOD = 4.5
export CORE_UTILIZATION = 50
export PLACE_DENSITY_LB_ADDON = 0.15
export SYNTH_REPEATABLE_BUILD = 1
export LEC_CHECK = 0
