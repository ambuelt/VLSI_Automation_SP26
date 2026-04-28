module fir_filter_tb;
    localparam int WIDTH = 16;
    localparam int N = 8;
    localparam int OUT_W = 2 * WIDTH + $clog2(N) + 1;
    localparam int LATENCY = 5;
    localparam int NUM_STIM = 16;
    localparam int TOTAL_CYCLES = NUM_STIM + LATENCY + 4;

    logic clk;
    logic rst;
    logic signed [WIDTH-1:0] x_in;
    logic signed [N-1:0][WIDTH-1:0] h;
    logic signed [OUT_W-1:0] y_out;

    logic signed [WIDTH-1:0] stim [0:NUM_STIM-1];
    logic signed [WIDTH-1:0] sample_model [0:N-1];
    logic signed [OUT_W-1:0] expected_pipe [0:LATENCY-1];

    integer cycle;
    integer i;
    integer idx;
    logic signed [OUT_W-1:0] expected_now;

    fir_filter #(
        .WIDTH(WIDTH),
        .N(N)
    ) dut (
        .clk(clk),
        .rst(rst),
        .x_in(x_in),
        .h(h),
        .y_out(y_out)
    );

    always #5 clk = ~clk;

    function automatic logic signed [OUT_W-1:0] model_dot;
        integer j;
        logic signed [OUT_W-1:0] acc;
        begin
            acc = '0;
            for (j = 0; j < N; j = j + 1) begin
                acc = acc + ($signed(sample_model[j]) * $signed(h[j]));
            end
            model_dot = acc;
        end
    endfunction

    initial begin
        clk = 1'b0;
        rst = 1'b1;
        x_in = '0;

        for (i = 0; i < N; i = i + 1) begin
            h[i] = i + 1;
            sample_model[i] = '0;
        end

        for (i = 0; i < LATENCY; i = i + 1) begin
            expected_pipe[i] = '0;
        end

        for (i = 0; i < NUM_STIM; i = i + 1) begin
            stim[i] = i + 1;
        end

        repeat (2) @(posedge clk);
        @(negedge clk);
        rst = 1'b0;

        for (cycle = 0; cycle < TOTAL_CYCLES; cycle = cycle + 1) begin
            @(negedge clk);
            if (cycle < NUM_STIM) begin
                x_in = stim[cycle];
            end else begin
                x_in = '0;
            end

            for (idx = N-1; idx > 0; idx = idx - 1) begin
                sample_model[idx] = sample_model[idx-1];
            end
            sample_model[0] = x_in;
            expected_now = model_dot();

            @(posedge clk);
            #1;
            if (cycle >= LATENCY) begin
                if (y_out !== expected_pipe[LATENCY-1]) begin
                    $display(
                        "FAIL: cycle %0d expected y_out=%0d got=%0d",
                        cycle, expected_pipe[LATENCY-1], y_out
                    );
                    $finish(1);
                end
            end else if (y_out !== '0) begin
                $display("FAIL: cycle %0d expected pipeline flush zero got=%0d", cycle, y_out);
                $finish(1);
            end

            for (idx = LATENCY-1; idx > 0; idx = idx - 1) begin
                expected_pipe[idx] = expected_pipe[idx-1];
            end
            expected_pipe[0] = expected_now;
        end

        $display("TB_PASS");
        $finish(0);
    end
endmodule
