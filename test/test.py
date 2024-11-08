# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import Timer
from cocotb.triggers import FallingEdge

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from cocotb.clock import Clock

@cocotb.test()
async def register_test(dut):
    dut._log.info("Starting basic register test")

    # Selecting basic register
    dut.uio_in.value = 0b00000000

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    await FallingEdge(dut.clk) # do stuff on the falling edge

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")
    dut._log.info("Start Register Test")

    # 1. Apply a value to bus, with n_load disabled (no load)
    dut.ui_in.value = 0b10101010
    dut.uio_in.value = dut.uio_in.value | 0b00010000  # Keep n_load disabled
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0, f"Expected output value does not match: {dut.uo_out.value}"

    # 2. Load a value into the register by asserting n_load (active low)
    dut._log.info("Loading value into the register")
    dut.uio_in.value = dut.uio_in.value & 0b11101111  # n_load active (low)
    await FallingEdge(dut.clk)
    dut.uio_in.value = dut.uio_in.value | 0b00010000  # Stop loading
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b10101010, f"Expected output value does not match: {dut.uo_out.value}"

    # 3. Change bus value and check that it doesn't load into register
    dut.ui_in.value = 0b01010101
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b10101010, f"Expected value to remain 0b10101010, got {dut.value.value}"

    # Load new value, skips old value
    dut.ui_in.value = 0b11111111

    # 4. Load a new value into the register
    dut._log.info("Loading new value into the register")
    dut.uio_in.value = dut.uio_in.value & 0b11101111  # n_load active (low)
    await FallingEdge(dut.clk)
    dut.uio_in.value = dut.uio_in.value | 0b00010000  # Stop loading
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b11111111, f"Expected value to be 0b11111111, got {dut.value.value}"

    # 5. Load same value into the register
    dut._log.info("Loading same value into the register again")
    dut.uio_in.value = dut.uio_in.value & 0b11101111  # n_load active (low)
    await FallingEdge(dut.clk)
    dut.uio_in.value = dut.uio_in.value | 0b00010000  # Stop loading
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b11111111, f"Expected value to remain 0b11111111, got {dut.value.value}"

    # Finish test after a few clock cycles
    dut._log.info("End Register Test")
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)


@cocotb.test()
async def input_mar_register_test(dut):
    dut._log.info("Start Input and MAR Test")

    # Selecting input and mar register
    dut.uio_in.value = 0b01000000

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    await FallingEdge(dut.clk) # do stuff on the falling edge

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")
    dut._log.info("Start Register Test")

    # 2. Load data into the data register (n_load_data active)
    dut._log.info("Loading data into data register")
    dut.ui_in.value = 0b10011011
    # dut.uio_in.value |= (1 << 5)
    # dut.uio_in.value &= ~(1 << 4)
    dut.uio_in.value = 0b01100000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b11
    # dut.uio_in.value |= (1 << 5)
    # dut.uio_in.value |= (1 << 4)
    dut.uio_in.value = 0b01110000
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b10011011, f"Expected data 0b10011011, got {dut.uo_out.value}"

    # 3. Load address into the addr register (n_load_addr active)
    dut._log.info("Loading address into addr register")
    dut.ui_in.value = 0b01010110
    # dut.uio_in.value = 0b01
    # dut.uio_in.value &= ~(1 << 5)
    # dut.uio_in.value |= (1 << 4)
    dut.uio_in.value = 0b01010000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b11
    # dut.uio_in.value |= (1 << 5)
    # dut.uio_in.value |= (1 << 4)
    dut.uio_in.value = 0b01110000
    await FallingEdge(dut.clk)
    assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b0110, f"Expected addr 0b0110, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

    # 4. Change bus, verify no load when load signals are high
    dut._log.info("Change bus, verify no load with high load signals")
    dut.ui_in.value = 0b11001001
    await FallingEdge(dut.clk)
    dut.ui_in.value = 0b11101011
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b10011011, f"Data should remain 0b10011011, got {dut.uo_out.value}"
    assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b0110, f"Addr should remain 0b0110, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

    # 5. Load both data and addr at the same time
    dut._log.info("Loading both data and addr simultaneously")
    # dut.uio_in.value = 0b00
    # dut.uio_in.value &= ~(1 << 5)
    # dut.uio_in.value &= ~(1 << 4)
    dut.uio_in.value = 0b01000000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b11
    # dut.uio_in.value |= (1 << 5)
    # dut.uio_in.value |= (1 << 4)
    dut.uio_in.value = 0b01110000
    await FallingEdge(dut.clk)
    assert dut.uo_out.value == 0b11101011, f"Expected data 0b11110000, got {dut.uo_out.value}"
    assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b1011, f"Expected addr 0b1011, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

    # Finish test
    dut._log.info("Finishing Input and MAR Test")
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)


@cocotb.test()
async def instruction_register_test(dut):
    dut._log.info("Starting instruction register test")

    # Selecting instruction register
    dut.uio_in.value = 0b10110000

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    await FallingEdge(dut.clk) # do stuff on the falling edge
    # TODO: Do we need a await Falling Edge at the start of every single test?

    # Reset
    dut._log.info("Applying reset")
    dut.ui_in.value = 0
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    # Test sequence

    # 1. Clear instruction register
    dut._log.info("Clearing instruction register")
    # dut.uio_in.value = 0b0111
    dut.uio_in.value = 0b10110000

    dut.rst_n.value = 1
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000

    dut.rst_n.value = 0
    await FallingEdge(dut.clk)

    # 2. Load a value into the instruction register (bus = 0b11001010)
    dut._log.info("Loading value into instruction register")
    # dut.uio_in.value = 0b1100
    dut.uio_in.value = 0b10100000
    
    dut.ui_in.value = 0b11001010
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000
    
    await FallingEdge(dut.clk)
    assert (int(dut.uio_out.value.binstr[4:8], 2) & 0xF) == 0b1100, f"Expected opcode 0b1100, got {(int(dut.uio_out.value.binstr[4:8], 2) & 0xF)}"

    # 3. Enable lower 4 bits onto the bus
    dut._log.info("Enabling lower 4 bits onto the bus")
    # dut.uio_in.value = 0b0010
    dut.uio_in.value = 0b10010000
    await FallingEdge(dut.clk)
    assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b1010, f"Expected bus lower 4 bits 0b1010, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000
    await FallingEdge(dut.clk)

    # Additional Test Cases

    # 4. Load a new value onto the bus
    dut._log.info("Loading new value onto the bus")
    dut.ui_in.value = 0b01100011
    # dut.uio_in.value = 0b1100
    dut.uio_in.value = 0b10100000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0010
    dut.uio_in.value = 0b10010000
    await FallingEdge(dut.clk)
    assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b0011, f"Expected bus lower 4 bits 0b0011, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000
    await FallingEdge(dut.clk)

    # 5. Enable and load in quick succession
    dut._log.info("Enabling and loading in quick succession")
    # dut.uio_in.value = 0b0010
    dut.uio_in.value = 0b10010000
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b1100
    dut.uio_in.value = 0b10100000
    dut.ui_in.value = 0b10000001
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0010
    dut.uio_in.value = 0b10010000
    await FallingEdge(dut.clk)
    assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b0001, f"Expected bus lower 4 bits 0b0001, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000
    await FallingEdge(dut.clk)
    
    # 6. Clear instruction register again
    dut._log.info("Clearing instruction register again")
    # dut.uio_in.value = 0b0111
    dut.uio_in.value = 0b10110000

    dut.rst_n.value = 1
    await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    dut.uio_in.value = 0b10110000

    dut.rst_n.value = 0
    assert (int(dut.uio_out.value.binstr[4:8], 2) & 0xF) == 0b0000, f"Expected opcode 0b0000, got {(int(dut.uio_out.value.binstr[4:8], 2) & 0xF)}"

    # Finish simulation
    dut._log.info("Finishing simulation")
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)

    

# @cocotb.test()
# async def instruction_register_test(dut):
    # dut._log.info("Starting instruction register test")

    # # Set the clock period to 10 ns (100 MHz)
    # clock = Clock(dut.clk, 10, units="ns")
    # cocotb.start_soon(clock.start())

    # await FallingEdge(dut.clk)

    # # Reset
    # dut._log.info("Applying reset")
    # dut.uio_in.value = 0b0110
    # dut.ui_in.value = 0
    # dut.rst_n.value = 0
    # await FallingEdge(dut.clk)
    # dut.rst_n.value = 1
    # await FallingEdge(dut.clk)

    # # Test sequence

    # # 1. Clear instruction register
    # dut._log.info("Clearing instruction register")
    # dut.uio_in.value = 0b0111
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)

    # # 2. Load a value into the instruction register (bus = 0b11001010)
    # dut._log.info("Loading value into instruction register")
    # dut.uio_in.value = 0b1100
    # dut.ui_in.value = 0b11001010
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)
    # assert (int(dut.uio_out.value.binstr[4:8], 2) & 0xF) == 0b1100, f"Expected opcode 0b1100, got {(int(dut.uio_out.value.binstr[4:8], 2) & 0xF)}"

    # # 3. Enable lower 4 bits onto the bus
    # dut._log.info("Enabling lower 4 bits onto the bus")
    # dut.uio_in.value = 0b0010
    # await FallingEdge(dut.clk)
    # assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b1010, f"Expected bus lower 4 bits 0b1010, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)

    # # Additional Test Cases

    # # 4. Load a new value onto the bus
    # dut._log.info("Loading new value onto the bus")
    # dut.ui_in.value = 0b01100011
    # dut.uio_in.value = 0b1100
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0010
    # await FallingEdge(dut.clk)
    # assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b0011, f"Expected bus lower 4 bits 0b0011, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)

    # # 5. Enable and load in quick succession
    # dut._log.info("Enabling and loading in quick succession")
    # dut.uio_in.value = 0b0010
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b1100
    # dut.ui_in.value = 0b10000001
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0010
    # await FallingEdge(dut.clk)
    # assert (int(dut.uo_out.value.binstr[-4:], 2) & 0xF) == 0b0001, f"Expected bus lower 4 bits 0b0001, got {(int(dut.uo_out.value.binstr[-4:], 2) & 0xF)}"
    # dut.uio_in.value = 0b0110
    # await FallingEdge(dut.clk)
    
    # # 6. Clear instruction register again
    # dut._log.info("Clearing instruction register again")
    # dut.uio_in.value = 0b0111
    # await FallingEdge(dut.clk)
    # dut.uio_in.value = 0b0110
    # assert (int(dut.uio_out.value.binstr[4:8], 2) & 0xF) == 0b0000, f"Expected opcode 0b0000, got {(int(dut.uio_out.value.binstr[4:8], 2) & 0xF)}"

    # # Finish simulation
    # dut._log.info("Finishing simulation")
    # await FallingEdge(dut.clk)
    # await FallingEdge(dut.clk)

# @cocotb.test()
# async def input_mar_register_test(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     await FallingEdge(dut.clk) # do stuff on the falling edge

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1
#     dut.ui_in.value = 0
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await FallingEdge(dut.clk)
#     dut.rst_n.value = 1

#     dut._log.info("Test project behavior")
#     dut._log.info("Start Register Test")

#     # 2. Load data into the data register (n_load_data active)
#     dut._log.info("Loading data into data register")
#     dut.ui_in.value = 0b10011011
#     dut.uio_in.value = 0b10
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 0b11
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b10011011, f"Expected data 0b10011011, got {dut.uo_out.value}"

#     # 3. Load address into the addr register (n_load_addr active)
#     dut._log.info("Loading address into addr register")
#     dut.ui_in.value = 0b01010110
#     dut.uio_in.value = 0b01
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 0b11
#     await FallingEdge(dut.clk)
#     assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b0110, f"Expected addr 0b0110, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

#     # 4. Change bus, verify no load when load signals are high
#     dut._log.info("Change bus, verify no load with high load signals")
#     dut.ui_in.value = 0b11001001
#     await FallingEdge(dut.clk)
#     dut.ui_in.value = 0b11101011
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b10011011, f"Data should remain 0b10011011, got {dut.uo_out.value}"
#     assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b0110, f"Addr should remain 0b0110, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

#     # 5. Load both data and addr at the same time
#     dut._log.info("Loading both data and addr simultaneously")
#     dut.uio_in.value = 0b00
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 0b11
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b11101011, f"Expected data 0b11110000, got {dut.uo_out.value}"
#     assert (int(dut.uio_out.value.binstr[-4:], 2) & 0xF) == 0b1011, f"Expected addr 0b1011, got {(int(dut.uio_out.value.binstr[-4:], 2) & 0xF)}"

#     # Finish simulation
#     dut._log.info("Finishing simulation")
#     await FallingEdge(dut.clk)
#     await FallingEdge(dut.clk)

# Simple Register Test
# @cocotb.test()
# async def register_test(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     await FallingEdge(dut.clk) # do stuff on the falling edge

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1
#     dut.ui_in.value = 0
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await FallingEdge(dut.clk)
#     dut.rst_n.value = 1

#     dut._log.info("Test project behavior")
#     dut._log.info("Start Register Test")

#     # 1. Apply a value to bus, with n_load disabled (no load)
#     dut.ui_in.value = 0b10101010
#     dut.uio_in.value = 1  # Keep n_load disabled
#     await FallingEdge(dut.clk)
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0, f"Expected output value does not match: {dut.uo_out.value}"

#     # 2. Load a value into the register by asserting n_load (active low)
#     dut._log.info("Loading value into the register")
#     dut.uio_in.value = 0  # n_load active (low)
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 1  # Stop loading
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b10101010, f"Expected output value does not match: {dut.uo_out.value}"

#     # 3. Change bus value and check that it doesn't load into register
#     dut.ui_in.value = 0b01010101
#     await FallingEdge(dut.clk)
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b10101010, f"Expected value to remain 0b10101010, got {dut.value.value}"

#     # Load new value, skips old value
#     dut.ui_in.value = 0b11111111

#     # 4. Load a new value into the register
#     dut._log.info("Loading new value into the register")
#     dut.uio_in.value = 0  # n_load active (low)
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 1  # Stop loading
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b11111111, f"Expected value to be 0b11111111, got {dut.value.value}"

#     # 5. Load same value into the register
#     dut._log.info("Loading same value into the register again")
#     dut.uio_in.value = 0  # n_load active (low)
#     await FallingEdge(dut.clk)
#     dut.uio_in.value = 1  # Stop loading
#     await FallingEdge(dut.clk)
#     assert dut.uo_out.value == 0b11111111, f"Expected value to remain 0b11111111, got {dut.value.value}"

#     # Finish simulation after a few clock cycles
#     dut._log.info("Finishing simulation")
#     await FallingEdge(dut.clk)
#     await FallingEdge(dut.clk)
