Iteration 1 physical summary for `fp16_multiplier`

- Result: PASS on final routed metrics
- Platform: `sky130hd`
- Clock target: `9 ns` via virtual clock
- CTS setup TNS: `-0.0246656`
- CTS hold TNS: `0`
- CTS setup WNS: `-0.0165379 ns`
- CTS hold WNS: `2.6942 ns`
- CTS setup violations: `2`
- CTS hold violations: `0`
- Global-route setup TNS: `-2.28477`
- Global-route hold TNS: `0`
- Global-route setup WNS: `-0.240957 ns`
- Global-route hold WNS: `2.54621 ns`
- Global-route setup violations: `15`
- Global-route hold violations: `0`
- Final setup TNS: `0`
- Final hold TNS: `0`
- Final setup WNS: `0.033662 ns`
- Final hold WNS: `2.5059 ns`
- Final setup violations: `0`
- Final hold violations: `0`
- Routed DRC errors: `0`
- Final flow errors: `0`
- Final utilization: `64.0960%`
- Final stdcell area: `8121.54 um^2`
- Final power: `0.00414275 W`

Notes:
- The design is combinational and has no real clock net in RTL.
- ORFS ran with a virtual clock to preserve the YAML `9 ns` timing target for I/O timing analysis.
- TritonCTS reported no valid clock nets, which is expected for this combinational module.
- Detailed routing converged to zero DRC errors and the extracted final timing report closed.

Artifacts retained:
- `output_physical/fp16_multiplier/fp16_multiplier.gds`
- `output_physical/fp16_multiplier/odb/fp16_multiplier_3_place.odb`
- `output_physical/fp16_multiplier/odb/fp16_multiplier_4_cts.odb`
- `output_physical/fp16_multiplier/odb/fp16_multiplier_5_route.odb`
- `results/fp16_multiplier.odb`
- `results/fp16_multiplier.gds`
- `results/fp16_multiplier.sdc`
