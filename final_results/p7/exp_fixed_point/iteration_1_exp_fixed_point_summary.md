# Physical Iteration 1 Summary

- Clock target held fixed at `4.5ns` in both SDC and `config.mk`.
- Config used: `CORE_UTILIZATION = 50`, `PLACE_DENSITY_LB_ADDON = 0.15`.
- CTS completed successfully and retained ODB exists at `output_physical/exp_fixed_point/odb/exp_fixed_point_4_cts.odb`.
- Routing completed successfully and retained ODB exists at `output_physical/exp_fixed_point/odb/exp_fixed_point_5_route.odb`.
- Final routed DRC violations: `0`.
- Placement congestion overflow: `0`.
- Detailed placement violations: `0`.
- Final area: `3088 um^2`.
- Final utilization: `52.4660%`.
- Final TNS: `0`.
- Final WNS: `1.84878`.
- Setup violation count: `0`.
- Hold violation count: `0`.
- Max slew violations: `0`.
- Max capacitance violations: `0`.
- Result: all targeted physical checks passed at the fixed YAML clock target.
