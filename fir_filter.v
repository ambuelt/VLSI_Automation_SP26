module fir_filter #(
    parameter WIDTH = 16,
    parameter N = 8
) (
    input  logic                              clk,
    input  logic                              rst,
    input  logic signed [WIDTH-1:0]           x_in,
    input  logic signed [N-1:0][WIDTH-1:0]    h,
    output logic signed [2*WIDTH+$clog2(N):0] y_out
);

    localparam int PROD_W = 2 * WIDTH;
    localparam int ACC_W  = 2 * WIDTH + $clog2(N) + 1;

    logic signed [WIDTH-1:0] sample_reg [0:N-1];
    logic signed [PROD_W-1:0] mult_reg [0:N-1];
    logic signed [ACC_W-1:0] sum2_reg [0:(N/2)-1];
    logic signed [ACC_W-1:0] sum4_reg [0:(N/4)-1];
    logic signed [ACC_W-1:0] sum8_reg;

    integer i;
    always_ff @(posedge clk) begin
        if (rst) begin
            for (i = 0; i < N; i = i + 1) begin
                sample_reg[i] <= '0;
                mult_reg[i] <= '0;
            end
            for (i = 0; i < (N / 2); i = i + 1) begin
                sum2_reg[i] <= '0;
            end
            for (i = 0; i < (N / 4); i = i + 1) begin
                sum4_reg[i] <= '0;
            end
            sum8_reg <= '0;
            y_out <= '0;
        end else begin
            sample_reg[0] <= x_in;
            for (i = 1; i < N; i = i + 1) begin
                sample_reg[i] <= sample_reg[i-1];
            end

            for (i = 0; i < N; i = i + 1) begin
                mult_reg[i] <= sample_reg[i] * h[i];
            end

            for (i = 0; i < (N / 2); i = i + 1) begin
                sum2_reg[i] <= $signed(mult_reg[2*i]) + $signed(mult_reg[2*i+1]);
            end

            for (i = 0; i < (N / 4); i = i + 1) begin
                sum4_reg[i] <= sum2_reg[2*i] + sum2_reg[2*i+1];
            end

            sum8_reg <= sum4_reg[0] + sum4_reg[1];
            y_out <= sum8_reg;
        end
    end

endmodule
