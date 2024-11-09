<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

The various registers used for a basic 8-bit CPU design.
Consists of a simple general purpose register, a memory address register, and an instruction register. The 3 registers are selected using the 6th and 7th uio pins.
| uio[7]       | uio[6]       | Selected Register |
|--------------|--------------|-------------------|
| 0  | 0  | General Purpose Register      |
| 0  | 1  | Memory Address Register      |
| 1  | 0  | Instruction Register      |

## Design Specifications

### Instruction Register

| Label                  | Input/Output | Description                                                                                      |
|------------------------|--------------|--------------------------------------------------------------------------------------------------|
| CLK [1 bit]            | Input        | Clock signal. Executes actions on rising edges.                                                  |
| W bus [8 bit]          | Input        | Takes 8 bits with the most significant 4 bits representing the opcode and the least significant 4 bits representing any other necessary value. Write them to the instruction register. |
| I [1 bit]              | Input        | Control signal that decides whether to read from the bus.                                        |
| I [1 bit]              | Input        | Control signal that decides tri-state buffer output to bus (drive register value if enabled, Z if disabled). |
| CLR [1 bit]            | Input        | Clears the instruction register’s data.                                                          |
| Instruction register[3:0] [4 bit] | Output | Output to W bus                                                                                  |
| Instruction register[7:4] [4 bit] | Output | Output to controller/sequences                                                                   |

- **Note**: All simulations pictured in this document were run using a 10 ns clock. The actual design will have a 100 ns clock.

#### Test Input Connections
| Test Input Name | Description  |
|-----------------|--------------|
| clk             | CLK          |
| ui_in[7:0]      | W bus        |
| uio_in [1]      | I            |
| uio_in [2]      | I            |
| uio_in [0]      | CLR          |
| uio_out[3:0]    | Instruction register[7:4] |
| uo_out[3:0]     | Instruction register[3:0] |

### Output Register

| Label                  | Input/Output | Description                                                                                      |
|------------------------|--------------|--------------------------------------------------------------------------------------------------|
| CLK [1 bit]            | Input        | Clock signal. Executes actions on rising edges.                                                  |
| W bus [8 bit]          | Input        | Data from the bus lines that are to be written to the Output register.                           |
| O [1 bit]              | Input        | Control signal that decides whether to read from the bus and load onto the output register.      |
| Output register [8 bit] | Output     | Register data that will be written to the binary display.                                        |

#### Test Input Connections
| Test Input Name | Description  |
|-----------------|--------------|
| clk             | CLK          |
| ui_in[7:0]      | W bus        |
| uio_in [0]      | O            |
| uo_out[7:0]     | Output register |

### B Register

| Label                  | Input/Output | Description                                                                                      |
|------------------------|--------------|--------------------------------------------------------------------------------------------------|
| CLK [1 bit]            | Input        | Clock signal. Executes actions on rising edges.                                                  |
| W bus [8 bit]          | Input        | Data from the bus lines that are to be written to the B register.                                |
| B [1 bit]              | Input        | Control signal that decides whether to read from the bus and load onto the B register.           |
| B register [8 bit]     | Output       | Register data that will be written to adder/subtractor.                                          |

#### Test Input Connections
| Test Input Name | Description  |
|-----------------|--------------|
| clk             | CLK          |
| ui_in[7:0]      | W bus        |
| uio_in [0]      | O            |
| uo_out[7:0]     | Output register |

### Input and MAR

| Label                  | Input/Output | Description                                                                                      |
|------------------------|--------------|--------------------------------------------------------------------------------------------------|
| CLK [1 bit]            | Input        | Clock signal. Executes actions on rising edges.                                                  |
| W bus [8 bit]          | Input        | Data from the bus lines that are to be written either Input or MAR register.                     |
| MD [1 bit]             | Input        | Control signal that decides if W bus data is to be written to the Input register. Should not be active at the same time as the MA control signal. |
| MA [1 bit]             | Input        | Control signal that decides if W bus data is to be written to the MAR register. Should not be active at the same time as the MD control signal. |
| Input register [8 bit] | Output       | Register data to be written to memory.                                                           |
| MAR [4 bit]            | Output       | Register data taken by RAM that controls where the data is to be written.                        |

#### Test Input Connections
| Test Input Name | Description  |
|-----------------|--------------|
| clk             | CLK          |
| ui_in[7:0]      | W bus        |
| uio_in [0]      | MD           |
| uio_in [1]      | MA           |
| uo_out[7:0]     | Input register |
| uio_out[3:0]    | MAR          |

