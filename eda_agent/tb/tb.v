`timescale 1ns/1ps

module tb;
    reg clk;
    reg reset;
    reg data_in;
    wire detected;

    reg [15:0] sample_input;
    reg [15:0] expected_output;
    integer i;

    seq_detector_0011 dut (
        .clk(clk),
        .reset(reset),
        .data_in(data_in),
        .detected(detected)
    );

    always #5 clk = ~clk;

    initial begin
        clk = 1'b0;
        reset = 1'b1;
        data_in = 1'b0;
        sample_input = 16'b0001100110110010;
        expected_output = 16'b0000010001000000;

        @(posedge clk);
        @(posedge clk);
        reset = 1'b0;

        for (i = 15; i >= 0; i = i - 1) begin
            data_in = sample_input[i];
            @(posedge clk);
            if (detected !== expected_output[i]) begin
                $display(
                    "FAIL cycle %0d: data_in=%b detected=%b expected=%b",
                    15 - i,
                    sample_input[i],
                    detected,
                    expected_output[i]
                );
                $finish(1);
            end
        end

        $display("PASS");
        $finish;
    end
endmodule
