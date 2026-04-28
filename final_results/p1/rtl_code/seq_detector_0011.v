module seq_detector_0011(
    input clk,
    input reset,
    input data_in,
    output reg detected
);

    reg [3:0] shift_reg;
    reg match_d;

    always @(posedge clk) begin
        if (reset) begin
            shift_reg <= 4'b0000;
            match_d <= 1'b0;
            detected <= 1'b0;
        end else begin
            detected <= match_d;
            match_d <= ({shift_reg[2:0], data_in} == 4'b0011);
            shift_reg <= {shift_reg[2:0], data_in};
        end
    end

endmodule
