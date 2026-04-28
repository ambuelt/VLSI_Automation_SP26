`timescale 1ns/1ps

module dot_product_tb;
    localparam integer LATENCY = 4;
    localparam integer NUM_VECTORS = 10;

    reg         clk;
    reg         rst;
    reg [63:0]  A;
    reg [63:0]  B;
    wire [19:0] dot_out;
    wire        valid;

    reg [19:0] expected_pipe [0:LATENCY-1];
    reg [63:0] vec_a [0:NUM_VECTORS-1];
    reg [63:0] vec_b [0:NUM_VECTORS-1];
    reg [19:0] expected_now;
    integer i;
    integer cycle_count;
    integer errors;

    dot_product dut (
        .clk(clk),
        .rst(rst),
        .A(A),
        .B(B),
        .dot_out(dot_out),
        .valid(valid)
    );

    always #5 clk = ~clk;

    function [19:0] calc_dot;
        input [63:0] vec_a;
        input [63:0] vec_b;
        integer idx;
        reg [19:0] acc;
        begin
            acc = 20'd0;
            for (idx = 0; idx < 8; idx = idx + 1) begin
                acc = acc + (vec_a[idx*8 +: 8] * vec_b[idx*8 +: 8]);
            end
            calc_dot = acc;
        end
    endfunction

    initial begin
        clk = 1'b0;
        rst = 1'b1;
        A = 64'd0;
        B = 64'd0;
        expected_now = 20'd0;
        cycle_count = 0;
        errors = 0;
        for (i = 0; i < LATENCY; i = i + 1) begin
            expected_pipe[i] = 20'd0;
        end

        vec_a[0] = 64'h0807060504030201;
        vec_b[0] = 64'h0102030405060708;
        vec_a[1] = 64'h1011121314151617;
        vec_b[1] = 64'h0807060504030201;
        vec_a[2] = 64'hFF00010203040506;
        vec_b[2] = 64'h0101010101010101;
        vec_a[3] = 64'h0001000100010001;
        vec_b[3] = 64'h0002000200020002;
        vec_a[4] = 64'h0011223344556677;
        vec_b[4] = 64'h8899AABBCCDDEEFF;
        vec_a[5] = 64'hFFFFFFFF00000000;
        vec_b[5] = 64'h00000000FFFFFFFF;
        vec_a[6] = 64'h7F7F7F7F7F7F7F7F;
        vec_b[6] = 64'h0101010101010101;
        vec_a[7] = 64'h123456789ABCDEF0;
        vec_b[7] = 64'h0F1E2D3C4B5A6978;
        vec_a[8] = 64'h0000000000000000;
        vec_b[8] = 64'hFFFFFFFFFFFFFFFF;
        vec_a[9] = 64'h0000000000000000;
        vec_b[9] = 64'h0000000000000000;

        repeat (2) @(posedge clk);
        rst = 1'b0;

        for (cycle_count = 0; cycle_count < NUM_VECTORS + LATENCY; cycle_count = cycle_count + 1) begin
            if (cycle_count < NUM_VECTORS) begin
                A = vec_a[cycle_count];
                B = vec_b[cycle_count];
                expected_now = calc_dot(vec_a[cycle_count], vec_b[cycle_count]);
            end else begin
                A = 64'd0;
                B = 64'd0;
                expected_now = 20'd0;
            end

            @(posedge clk);
            for (i = LATENCY - 1; i > 0; i = i - 1) begin
                expected_pipe[i] = expected_pipe[i-1];
            end
            expected_pipe[0] = expected_now;

            #1;
            if (valid && dot_out !== expected_pipe[LATENCY-1]) begin
                $display("TB_FAIL: expected %0d got %0d at cycle %0d", expected_pipe[LATENCY-1], dot_out, cycle_count);
                errors = errors + 1;
            end
        end

        if (errors == 0) begin
            $display("TB_PASS");
        end else begin
            $display("TB_FAIL: %0d mismatches", errors);
        end
        $finish;
    end
endmodule
