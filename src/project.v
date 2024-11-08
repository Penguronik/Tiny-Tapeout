/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_ronikant_jeremykam_tinyregisters (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // uio pins: 
    // 7:6 chip select inputs
    // 5:4 extra inputs
    // 3:0 extra outputs
    assign uio_oe  = 8'b00001111;

    // Decoder
    wire [2:0] decoder_out_n;
    wire [1:0] select_register = uio_in[7:6];
    assign decoder_out_n = (select_register == 0) ? 3'b110 :
        (select_register == 1) ? 3'b101 : 
        (select_register == 2) ? 3'b011 : 3'b111;

    // Mux
    wire [7:0] register_out;
    wire [7:0] MAR_data_out;
    wire [3:0] MAR_addr_out;
    wire [7:0] IR_bus_out;
    wire [3:0] IR_opcode_out;
    assign uo_out = (select_register == 0) ? register_out :
        (select_register == 1) ? MAR_data_out :
        (select_register == 2) ? IR_bus_out : 8'b00000000;
    assign uio_out[3:0] = (select_register == 1) ? MAR_addr_out :
        (select_register == 2) ? IR_opcode_out : 4'b0000;
    
    // Register
    register register(.clk(clk),.n_load(uio_in[4] | decoder_out_n[0]),.bus(ui_in),.value(register_out));

    // Input and MAR Register
    input_mar_register im_register( .clk(clk), .n_load_data(uio_in[4] | decoder_out_n[1]), .n_load_addr(uio_in [5] | decoder_out_n[1]), .bus(ui_in), .data(MAR_data_out), .addr(MAR_addr_out) );

    // Instruction Register Start
    wire [7:0] bus;
    instruction_register instr_register( .clk(clk), .clear(rst_n), .n_load(uio_in [4] | decoder_out_n[2]), .n_enable(uio_in [5] | decoder_out_n[2]), .bus(bus), .opcode(IR_opcode_out) );
    assign bus = ((uio_in [5] | decoder_out_n[2]) == 0) ? 8'bz : ui_in;           // Input path
    assign IR_bus_out = bus;                                // Output path

    
    // All output pins must be assigned. If not used, assign to 0.
    assign uio_out[7:4] = 0;
    
    // List all unused inputs to prevent warnings
    wire _unused = &{ena, uio_in[3:0], 1'b0};
    // Register Test End
    
    
endmodule
