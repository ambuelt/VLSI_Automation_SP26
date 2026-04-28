create_clock -name clk -period 1.1 [get_ports clk]
set_input_delay 0 -clock clk [get_ports {reset data_in}]
set_output_delay 0 -clock clk [get_ports detected]
