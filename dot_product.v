module dot_product (
    input  wire        clk,
    input  wire        rst,
    input  wire [63:0] A,
    input  wire [63:0] B,
    output reg  [19:0] dot_out,
    output reg         valid
);
    integer i;

    reg [15:0] mult_s1 [0:7];
    reg [16:0] sum_s2 [0:3];
    reg [17:0] sum_s3 [0:1];
    reg [19:0] sum_s4;
    reg [3:0]  valid_pipe;

    wire [7:0] a_lane [0:7];
    wire [7:0] b_lane [0:7];

    assign a_lane[0] = A[7:0];
    assign a_lane[1] = A[15:8];
    assign a_lane[2] = A[23:16];
    assign a_lane[3] = A[31:24];
    assign a_lane[4] = A[39:32];
    assign a_lane[5] = A[47:40];
    assign a_lane[6] = A[55:48];
    assign a_lane[7] = A[63:56];

    assign b_lane[0] = B[7:0];
    assign b_lane[1] = B[15:8];
    assign b_lane[2] = B[23:16];
    assign b_lane[3] = B[31:24];
    assign b_lane[4] = B[39:32];
    assign b_lane[5] = B[47:40];
    assign b_lane[6] = B[55:48];
    assign b_lane[7] = B[63:56];

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            for (i = 0; i < 8; i = i + 1) begin
                mult_s1[i] <= 16'd0;
            end
            for (i = 0; i < 4; i = i + 1) begin
                sum_s2[i] <= 17'd0;
            end
            for (i = 0; i < 2; i = i + 1) begin
                sum_s3[i] <= 18'd0;
            end
            sum_s4    <= 20'd0;
            dot_out   <= 20'd0;
            valid_pipe <= 4'b0000;
            valid     <= 1'b0;
        end else begin
            for (i = 0; i < 8; i = i + 1) begin
                mult_s1[i] <= a_lane[i] * b_lane[i];
            end

            sum_s2[0] <= mult_s1[0] + mult_s1[1];
            sum_s2[1] <= mult_s1[2] + mult_s1[3];
            sum_s2[2] <= mult_s1[4] + mult_s1[5];
            sum_s2[3] <= mult_s1[6] + mult_s1[7];

            sum_s3[0] <= sum_s2[0] + sum_s2[1];
            sum_s3[1] <= sum_s2[2] + sum_s2[3];

            sum_s4    <= sum_s3[0] + sum_s3[1];
            dot_out   <= sum_s4;

            valid_pipe <= {valid_pipe[2:0], 1'b1};
            valid      <= valid_pipe[3];
        end
    end
endmodule
