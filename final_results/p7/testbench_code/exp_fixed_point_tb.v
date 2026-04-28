module exp_fixed_point_tb;
  localparam int WIDTH = 8;
  localparam int FRAC_BITS = WIDTH - 1;
  localparam int SCALE = 1 << FRAC_BITS;

  logic clk;
  logic rst;
  logic enable;
  logic [WIDTH-1:0] x_in;
  logic [2*WIDTH-1:0] exp_out;

  int cycle_count;
  int expected_stage0;
  bit valid_stage0;

  exp_fixed_point #(
    .WIDTH(WIDTH)
  ) dut (
    .clk(clk),
    .rst(rst),
    .enable(enable),
    .x_in(x_in),
    .exp_out(exp_out)
  );

  function automatic int expected_exp(input int x_value);
    int square_term;
    int cube_term;
    begin
      square_term = (x_value * x_value) >> WIDTH;
      cube_term = (x_value * x_value * x_value) / (6 * SCALE * SCALE);
      expected_exp = SCALE + x_value + square_term + cube_term;
    end
  endfunction

  task automatic drive_sample(input int x_value);
    begin
      @(negedge clk);
      enable = 1'b1;
      x_in = x_value[WIDTH-1:0];
    end
  endtask

  task automatic idle_cycle;
    begin
      @(negedge clk);
      enable = 1'b0;
      x_in = '0;
    end
  endtask

  always #5 clk = ~clk;

  always @(posedge clk) begin
    cycle_count = cycle_count + 1;
    #1;

    if (rst) begin
      valid_stage0 = 1'b0;
      expected_stage0 = 0;
    end else begin
      if (valid_stage0) begin
        if (exp_out !== expected_stage0) begin
          $display("Mismatch at cycle %0d: expected %0d got %0d", cycle_count, expected_stage0, exp_out);
          $fatal(1);
        end
      end

      valid_stage0 = enable;
      expected_stage0 = expected_exp(x_in);
    end
  end

  initial begin
    clk = 1'b0;
    rst = 1'b1;
    enable = 1'b0;
    x_in = '0;
    cycle_count = 0;
    expected_stage0 = 0;
    valid_stage0 = 1'b0;

    repeat (2) @(posedge clk);
    @(negedge clk);
    rst = 1'b0;

    drive_sample(0);
    drive_sample(8'd32);
    drive_sample(8'd64);
    drive_sample(8'd96);
    drive_sample(8'd128);
    drive_sample(8'd160);
    drive_sample(8'd192);
    drive_sample(8'd255);

    idle_cycle();
    idle_cycle();
    idle_cycle();

    $display("PASS");
    $finish;
  end
endmodule
