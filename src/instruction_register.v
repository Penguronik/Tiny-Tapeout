module instruction_register(
  input clk, clear, n_load, n_enable,
  inout [7:0] bus,
  output [3:0] opcode
);
  reg [7:0] instruction;
  
  assign bus[3:0] = !n_enable ? instruction[3:0] : 4'bZ;
  assign opcode = instruction[7:4];
  
  always@(posedge clk) begin
    if (clear) instruction <= 8'b0;
    else if (!n_load) instruction <= bus;
  end

endmodule

