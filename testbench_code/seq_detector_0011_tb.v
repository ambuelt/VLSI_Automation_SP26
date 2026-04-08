`timescale 1ns/1ps

module seq_detector_0011_tb;
    localparam integer SAMPLE_LEN = 16;
    localparam [SAMPLE_LEN-1:0] SAMPLE_INPUT = 16'b0001100110110010;
    localparam [SAMPLE_LEN-1:0] SAMPLE_OUTPUT = 16'b0000010001000000;
    localparam [SAMPLE_LEN-1:0] OVERLAP_INPUT = 16'b0011001100110011;
    localparam [SAMPLE_LEN-1:0] OVERLAP_OUTPUT = 16'b0000100010001000;

    reg clk;
    reg reset;
    reg data_in;
    wire detected;

    integer i;

    seq_detector_0011 dut (
        .clk(clk),
        .reset(reset),
        .data_in(data_in),
        .detected(detected)
    );

    always #5 clk = ~clk;

    task check_sample_stream;
        input [SAMPLE_LEN-1:0] input_bits;
        input [SAMPLE_LEN-1:0] expected_bits;
        begin
            for (i = SAMPLE_LEN - 1; i >= 0; i = i - 1) begin
                @(negedge clk);
                data_in = input_bits[i];
                @(posedge clk);
                #1;
                if (detected !== expected_bits[i]) begin
                    $display(
                        "FAIL cycle %0d: data_in=%b detected=%b expected=%b",
                        SAMPLE_LEN - 1 - i,
                        input_bits[i],
                        detected,
                        expected_bits[i]
                    );
                    $finish(1);
                end
            end
        end
    endtask

    initial begin
        clk = 1'b0;
        reset = 1'b1;
        data_in = 1'b0;

        repeat (2) begin
            @(posedge clk);
            #1;
            if (detected !== 1'b0) begin
                $display("FAIL during reset: detected=%b expected=0", detected);
                $finish(1);
            end
        end

        reset = 1'b0;
        check_sample_stream(SAMPLE_INPUT, SAMPLE_OUTPUT);

        @(negedge clk);
        reset = 1'b1;
        data_in = 1'b1;
        @(posedge clk);
        #1;
        if (detected !== 1'b0) begin
            $display("FAIL after reset pulse: detected=%b expected=0", detected);
            $finish(1);
        end

        reset = 1'b0;
        check_sample_stream(OVERLAP_INPUT, OVERLAP_OUTPUT);

        $display("PASS");
        $finish;
    end
endmodule
