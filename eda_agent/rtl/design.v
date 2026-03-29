module seq_detector_0011(
    input clk,
    input reset,
    input data_in,
    output reg detected
);

    reg [1:0] state;

    localparam S_IDLE = 2'd0;
    localparam S_0    = 2'd1;
    localparam S_00   = 2'd2;
    localparam S_001  = 2'd3;

    always @(posedge clk) begin
        if (reset) begin
            state <= S_IDLE;
            detected <= 1'b0;
        end else begin
            detected <= 1'b0;

            case (state)
                S_IDLE: begin
                    if (data_in == 1'b0) begin
                        state <= S_0;
                    end else begin
                        state <= S_IDLE;
                    end
                end

                S_0: begin
                    if (data_in == 1'b0) begin
                        state <= S_00;
                    end else begin
                        state <= S_IDLE;
                    end
                end

                S_00: begin
                    if (data_in == 1'b1) begin
                        state <= S_001;
                    end else begin
                        state <= S_00;
                    end
                end

                S_001: begin
                    if (data_in == 1'b1) begin
                        detected <= 1'b1;
                        state <= S_IDLE;
                    end else begin
                        state <= S_0;
                    end
                end

                default: begin
                    state <= S_IDLE;
                    detected <= 1'b0;
                end
            endcase
        end
    end

endmodule
