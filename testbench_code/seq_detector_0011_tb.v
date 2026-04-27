module seq_detector_0011_tb;
    localparam integer SAMPLE_LEN = 16;

    reg clk;
    reg reset;
    reg data_in;
    wire detected;

    reg [SAMPLE_LEN-1:0] sample_input;
    reg [SAMPLE_LEN-1:0] sample_output;
    integer idx;

    seq_detector_0011 dut (
        .clk(clk),
        .reset(reset),
        .data_in(data_in),
        .detected(detected)
    );

    always #5 clk = ~clk;

    task check_cycle;
        input reg bit_in;
        input reg expected_detected;
        begin
            @(negedge clk);
            data_in = bit_in;
            @(posedge clk);
            #1;
            if (detected !== expected_detected) begin
                $display(
                    "FAIL: bit=%0b expected detected=%0b got=%0b at time %0t",
                    bit_in,
                    expected_detected,
                    detected,
                    $time
                );
                $finish(1);
            end
        end
    endtask

    initial begin
        clk = 1'b0;
        reset = 1'b1;
        data_in = 1'b0;
        sample_input = 16'b0001100110110010;
        sample_output = 16'b0000010001000000;

        @(posedge clk);
        #1;
        if (detected !== 1'b0) begin
            $display("FAIL: detected should clear during reset");
            $finish(1);
        end

        @(negedge clk);
        reset = 1'b0;

        for (idx = 0; idx < SAMPLE_LEN; idx = idx + 1) begin
            check_cycle(
                sample_input[SAMPLE_LEN - 1 - idx],
                sample_output[SAMPLE_LEN - 1 - idx]
            );
        end

        check_cycle(1'b0, 1'b0);
        check_cycle(1'b0, 1'b0);
        check_cycle(1'b1, 1'b0);
        check_cycle(1'b1, 1'b0);
        check_cycle(1'b1, 1'b1);

        @(negedge clk);
        reset = 1'b1;
        data_in = 1'b1;
        @(posedge clk);
        #1;
        if (detected !== 1'b0) begin
            $display("FAIL: detected should clear after synchronous reset");
            $finish(1);
        end

        @(negedge clk);
        reset = 1'b0;
        check_cycle(1'b0, 1'b0);
        check_cycle(1'b0, 1'b0);
        check_cycle(1'b1, 1'b0);
        check_cycle(1'b1, 1'b0);
        check_cycle(1'b0, 1'b1);

        $display("PASS");
        $finish;
    end
endmodule
