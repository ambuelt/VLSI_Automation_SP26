Iteration 1 used `CLOCK_PERIOD = 1.1`, `CORE_UTILIZATION = 10`, and `PLACE_DENSITY_LB_ADDON = 0.05`.

Observed results:
- Final area: `220.211 um^2` stdcell area
- Final utilization: `0.167142`
- Final power: `0.000414627 W`
- Final TNS: `0`
- Final WNS: `0.124171`
- Setup violation count: `0`
- Hold violation count: `0`
- Detailed placement violations: `0`
- Congestion overflow: `0`
- CTS status: completed successfully
- Routing status: completed successfully
- Routed DRC violations: `0`
- Retained CTS ODB: `output_physical/seq_detector_0011/odb/seq_detector_0011_4_cts.odb`
- Retained routed ODB: `output_physical/seq_detector_0011/odb/seq_detector_0011_5_route.odb`
- Retained GDS: `output_physical/seq_detector_0011/seq_detector_0011.gds`

Constraint note:
- The YAML fixed the clock target at `1.1 ns` but did not specify external I/O delay budgets.
- This run therefore kept the YAML clock unchanged and used zero external input/output delays rather than the earlier placeholder values.

Outcome:
- All targeted post-CTS and routed checks passed in this iteration.
