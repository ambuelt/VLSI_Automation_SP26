module seq_detector_0011 (clk,
    data_in,
    detected,
    reset);
 input clk;
 input data_in;
 output detected;
 input reset;

 wire _00_;
 wire _01_;
 wire _02_;
 wire _03_;
 wire _04_;
 wire _05_;
 wire net1;
 wire net3;
 wire match_d;
 wire net2;
 wire \shift_reg[0] ;
 wire \shift_reg[1] ;
 wire \shift_reg[2] ;
 wire clknet_0_clk;
 wire clknet_1_0__leaf_clk;
 wire clknet_1_1__leaf_clk;

 sky130_fd_sc_hd__nor2b_2 _06_ (.A(net2),
    .B_N(\shift_reg[0] ),
    .Y(_00_));
 sky130_fd_sc_hd__and2b_2 _07_ (.A_N(net2),
    .B(net1),
    .X(_01_));
 sky130_fd_sc_hd__and2b_2 _08_ (.A_N(net2),
    .B(match_d),
    .X(_02_));
 sky130_fd_sc_hd__and2b_2 _09_ (.A_N(net2),
    .B(\shift_reg[1] ),
    .X(_03_));
 sky130_fd_sc_hd__nor2_1 _10_ (.A(\shift_reg[1] ),
    .B(\shift_reg[2] ),
    .Y(_05_));
 sky130_fd_sc_hd__and3_1 _11_ (.A(net1),
    .B(_00_),
    .C(_05_),
    .X(_04_));
 sky130_fd_sc_hd__clkbuf_4 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__clkbuf_4 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__clkbuf_4 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkbuf_1 clkload0 (.A(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \detected$_SDFF_PP0_  (.D(_02_),
    .Q(net3),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input1 (.A(data_in),
    .X(net1));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input2 (.A(reset),
    .X(net2));
 sky130_fd_sc_hd__dfxtp_1 \match_d$_SDFF_PP0_  (.D(_04_),
    .Q(match_d),
    .CLK(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output3 (.A(net3),
    .X(detected));
 sky130_fd_sc_hd__dfxtp_1 \shift_reg[0]$_SDFF_PP0_  (.D(_01_),
    .Q(\shift_reg[0] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \shift_reg[1]$_SDFF_PP0_  (.D(_00_),
    .Q(\shift_reg[1] ),
    .CLK(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__dfxtp_1 \shift_reg[2]$_SDFF_PP0_  (.D(_03_),
    .Q(\shift_reg[2] ),
    .CLK(clknet_1_0__leaf_clk));
endmodule
