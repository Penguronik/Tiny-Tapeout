# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import Timer
from cocotb.triggers import FallingEdge

@cocotb.test()
async def input_and_mar_test(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    await FallingEdge(dut.clk)

    # Test sequence

    # 1. Apply a value to bus, with both load signals disabled (no load)
    dut._log.info("Check no load when both load signals are high")
    dut.bus.value = 0b10101010
    dut.n_load_data.value = 1
    dut.n_load_addr.value = 1
    await FallingEdge(dut.clk)
    dut.bus.value = 0b10011011
    await FallingEdge(dut.clk)
    assert dut.data.value == 0, f"Data should remain unchanged, got {dut.data.value}"
    assert dut.addr.value == 0, f"Addr should remain unchanged, got {dut.addr.value}"

    # 2. Load data into the data register (n_load_data active)
    dut._log.info("Loading data into data register")
    dut.bus.value = 0b10101010
    dut.n_load_data.value = 0
    await FallingEdge(dut.clk)
    dut.n_load_data.value = 1
    await FallingEdge(dut.clk)
    assert dut.data.value == 0b10101010, f"Expected data 0b10101010, got {dut.data.value}"

    # 3. Load address into the addr register (n_load_addr active)
    dut._log.info("Loading address into addr register")
    dut.bus.value = 0b01010110
    dut.n_load_addr.value = 0
    await FallingEdge(dut.clk)
    dut.n_load_addr.value = 1
    await FallingEdge(dut.clk)
    assert dut.addr.value == 0b0101, f"Expected addr 0b0101, got {dut.addr.value}"

    # 4. Change bus, verify no load when load signals are high
    dut._log.info("Change bus, verify no load with high load signals")
    dut.bus.value = 0b11001001
    await FallingEdge(dut.clk)
    dut.bus.value = 0b11101011
    await FallingEdge(dut.clk)
    assert dut.data.value == 0b10101010, f"Data should remain 0b10101010, got {dut.data.value}"
    assert dut.addr.value == 0b0101, f"Addr should remain 0b0101, got {dut.addr.value}"

    # 5. Load both data and addr at the same time
    dut._log.info("Loading both data and addr simultaneously")
    dut.bus.value = 0b11110000
    dut.n_load_data.value = 0
    dut.n_load_addr.value = 0
    await FallingEdge(dut.clk)
    dut.n_load_data.value = 1
    dut.n_load_addr.value = 1
    await FallingEdge(dut.clk)
    assert dut.data.value == 0b11110000, f"Expected data 0b11110000, got {dut.data.value}"
    assert dut.addr.value == 0b1111, f"Expected addr 0b1111, got {dut.addr.value}"

    # Finish simulation
    dut._log.info("Finishing simulation")
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)


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


# async def test_project(dut):
#     dut._log.info("Start")

#     # Set the clock period to 10 us (100 KHz)
#     clock = Clock(dut.clk, 10, units="us")
#     cocotb.start_soon(clock.start())

#     # Reset
#     dut._log.info("Reset")
#     dut.ena.value = 1
#     dut.ui_in.value = 0
#     dut.uio_in.value = 0
#     dut.rst_n.value = 0
#     await ClockCycles(dut.clk, 10)
#     dut.rst_n.value = 1

#     dut._log.info("Test project behavior")

#     # Set the input values you want to test
#     dut.ui_in.value = 0b01011010
#     dut.uio_in.value = 0b00000000

#     # Wait for one clock cycle to see the output values
#     await ClockCycles(dut.clk, 1)

#     dut.uio_in.value = 0b00000001
#     dut.ui_in.value = 0b01101110

#     # Wait for one clock cycle to see the output values
#     await ClockCycles(dut.clk, 1)

#     # The following assersion is just an example of how to check the output values.
#     # Change it to match the actual expected output of your module:
#     assert dut.uo_out.value == 0b01011010

#     # Keep testing the module by changing the input values, waiting for
#     # one or more clock cycles, and asserting the expected output values.
