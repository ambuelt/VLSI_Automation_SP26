module fp16_multiplier(
    input  wire [15:0] a,
    input  wire [15:0] b,
    output wire [15:0] result
);
    function [15:0] fp16_mul;
        input [15:0] x;
        input [15:0] y;

        reg        sign;
        reg [4:0]  exp_x;
        reg [4:0]  exp_y;
        reg [9:0]  frac_x;
        reg [9:0]  frac_y;
        reg [10:0] mant_x;
        reg [10:0] mant_y;
        reg [21:0] product;
        reg signed [7:0] exp_sum;
        reg signed [7:0] exp_norm;
        reg [10:0] mant_main;
        reg        guard_bit;
        reg        round_bit;
        reg        sticky_bit;
        reg [11:0] rounded_mant;
        begin
            sign   = x[15] ^ y[15];
            exp_x  = x[14:10];
            exp_y  = y[14:10];
            frac_x = x[9:0];
            frac_y = y[9:0];

            if ((exp_x == 5'd0 && frac_x == 10'd0) || (exp_y == 5'd0 && frac_y == 10'd0)) begin
                fp16_mul = 16'd0;
            end else if (exp_x == 5'h1f || exp_y == 5'h1f) begin
                fp16_mul = {sign, 5'h1f, 10'd0};
            end else begin
                mant_x  = (exp_x == 5'd0) ? {1'b0, frac_x} : {1'b1, frac_x};
                mant_y  = (exp_y == 5'd0) ? {1'b0, frac_y} : {1'b1, frac_y};
                exp_sum = $signed({1'b0, exp_x}) + $signed({1'b0, exp_y}) - 8'sd15;
                product = mant_x * mant_y;

                if (product[21]) begin
                    exp_norm   = exp_sum + 8'sd1;
                    mant_main  = product[21:11];
                    guard_bit  = product[10];
                    round_bit  = product[9];
                    sticky_bit = |product[8:0];
                end else begin
                    exp_norm   = exp_sum;
                    mant_main  = product[20:10];
                    guard_bit  = product[9];
                    round_bit  = product[8];
                    sticky_bit = |product[7:0];
                end

                rounded_mant = {1'b0, mant_main};
                if (guard_bit && (round_bit || sticky_bit || mant_main[0])) begin
                    rounded_mant = rounded_mant + 12'd1;
                end

                if (rounded_mant[11]) begin
                    rounded_mant = rounded_mant >> 1;
                    exp_norm     = exp_norm + 8'sd1;
                end

                if (exp_norm >= 8'sd31) begin
                    fp16_mul = {sign, 5'h1f, 10'd0};
                end else if (exp_norm <= 8'sd0) begin
                    fp16_mul = 16'd0;
                end else begin
                    fp16_mul = {sign, exp_norm[4:0], rounded_mant[9:0]};
                end
            end
        end
    endfunction

    assign result = fp16_mul(a, b);
endmodule
