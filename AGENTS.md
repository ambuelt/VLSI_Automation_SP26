Agent: Spec2RTL

Goal:
Convert hardware specifications into working RTL and verify using simulation.

Steps:
1. Read input .yaml for module description, ports, and I/O requirements
2. Generate Verilog RTL
3. Write RTL to rtl/design.v
4. Run simulation
5. If simulation fails, debug and regenerate RTL