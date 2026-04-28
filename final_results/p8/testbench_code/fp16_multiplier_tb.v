`timescale 1ns/1ps

module fp16_multiplier_tb;
    reg  [15:0] a;
    reg  [15:0] b;
    wire [15:0] result;

    integer i;
    integer errors;
    reg [15:0] rand_a;
    reg [15:0] rand_b;
    reg [4:0]  rand_exp_a;
    reg [4:0]  rand_exp_b;
    reg [9:0]  rand_frac_a;
    reg [9:0]  rand_frac_b;

    fp16_multiplier dut (
        .a(a),
        .b(b),
        .result(result)
    );

    function [15:0] ref_mul;
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
                ref_mul = 16'd0;
            end else if (exp_x == 5'h1f || exp_y == 5'h1f) begin
                ref_mul = {sign, 5'h1f, 10'd0};
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
                    ref_mul = {sign, 5'h1f, 10'd0};
                end else if (exp_norm <= 8'sd0) begin
                    ref_mul = 16'd0;
                end else begin
                    ref_mul = {sign, exp_norm[4:0], rounded_mant[9:0]};
                end
            end
        end
    endfunction

    task check_case;
        input [15:0] aa;
        input [15:0] bb;
        reg   [15:0] expected;
        begin
            a = aa;
            b = bb;
            expected = ref_mul(aa, bb);
            #1;
            if (result !== expected) begin
                $display("TB_FAIL a=%h b=%h expected=%h got=%h", aa, bb, expected, result);
                errors = errors + 1;
            end
        end
    endtask

    initial begin
        errors = 0;

        check_case(16'h0000, 16'h4000);
        check_case(16'h3c00, 16'h4000);
        check_case(16'hbc00, 16'h4000);
        check_case(16'h3e00, 16'h4000);
        check_case(16'h3e00, 16'h3e00);
        check_case(16'h3800, 16'h3800);
        check_case(16'h3555, 16'h4200);
        check_case(16'h7bff, 16'h3c00);
        check_case(16'h7bff, 16'h7bff);
        check_case(16'h0400, 16'h0400);

        for (i = 0; i < 100; i = i + 1) begin
            rand_exp_a = (i % 30) + 1;
            rand_exp_b = ((i * 3) % 30) + 1;
            rand_frac_a = i;
            rand_frac_b = (i * 7);
            rand_a = {1'b0, rand_exp_a, rand_frac_a};
            rand_b = {1'b0, rand_exp_b, rand_frac_b};
            check_case(rand_a, rand_b);

            rand_exp_a = ((i * 5) % 30) + 1;
            rand_exp_b = ((i * 9) % 30) + 1;
            rand_frac_a = (i * 11);
            rand_frac_b = (i * 13);
            rand_a = {1'b1, rand_exp_a, rand_frac_a};
            rand_b = {1'b0, rand_exp_b, rand_frac_b};
            check_case(rand_a, rand_b);
        end

        if (errors == 0) begin
            $display("TB_PASS");
        end else begin
            $display("TB_FAIL: %0d mismatches", errors);
        end
        $finish;
    end
endmodule
