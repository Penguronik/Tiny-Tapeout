module register(
  input clk, n_load,
  input [7:0] bus,
  output reg [7:0] value
);
  
  always@(posedge clk) begin
    if (!n_load) value <= bus;
  end

endmodule