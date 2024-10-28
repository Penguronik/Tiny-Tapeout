/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // // Register Test Start
    // register b_register(.clk(clk),.n_load(uio_in [0]),.bus(ui_in),.value(uo_out));
    
    // // All output pins must be assigned. If not used, assign to 0.
    // // assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
    // assign uio_out = 0;
    // assign uio_oe  = 0;
    
    // // List all unused inputs to prevent warnings
    // wire _unused = &{ena, rst_n, uio_in[7:1], 1'b0};
    // // Register Test End

    
    // Input and MAR Register Start
    input_mar_register im_register( .clk(clk), .n_load_data(uio_in [0]), .n_load_addr(uio_in [1]), .bus(ui_in), .data(uo_out), .addr(uio_out[3:0]) );
    
    // All output pins must be assigned. If not used, assign to 0.
    assign uio_oe = 0;
    assign uio_out[7:4] = 0;
    
    // List all unused inputs to prevent warnings
    wire _unused = &{ena, rst_n, uio_in[7:2], 1'b0};
    // Input and MAR Register End

    
    // // Instruction Register Start
    // wire [7:0] bus;
    
    // instruction_register instr_register( .clk(clk), .clear(uio_in [0]), .n_load(uio_in [1]), .n_enable(uio_in [2]), .bus(bus), .opcode(uio_out[3:0]) );
    
    // assign bus = (uio_in[3] == 8'b00000001) ? ui_in : 8'bz; // Input path
    // assign uo_out = bus;                                    // Output path
    // // assign uio_oe = {8{!ui_in[1]}};                       // Enable path based on n_enable
    
    // // All output pins must be assigned. If not used, assign to 0.
    // assign uio_oe  = 0;
    
    // // List all unused inputs to prevent warnings
    // wire _unused = &{ena, rst_n, 1'b0};
    // // Instruction Register End
    
endmodule
