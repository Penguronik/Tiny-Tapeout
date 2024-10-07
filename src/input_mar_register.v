module input_mar_register(
  input clk, n_load_data, n_load_addr,
  input [7:0] bus,
  output reg [7:0] data,
  output reg [3:0] addr
);
  
  always@(posedge clk) begin
    if(!n_load_data) data <= bus;
    if(!n_load_addr) addr <= bus[3:0];
  end
endmodule