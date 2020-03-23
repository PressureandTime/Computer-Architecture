"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.mar = 0
        self.mdr = 0
        self.running = True

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,  #RO
            0b00001000,  # 8
            0b01000111,  # PRN R0
            0b00000000,  # RO
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, index):
        self.mar = index
        self.mdr = self.ram[self.mar]
        return self.mdr

    def ram_write(self, index, value):
        self.mar = index
        self.mdr = value
        self.ram[self.mar] = self.mdr

    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'LDI':
            self.reg[reg_a] = reg_b
        elif op == 'PRN':
            print(self.reg[reg_a])
        elif op == 'HLT':
            self.running = False
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" %
              (self.pc, self.ram_read(self.pc), self.ram_read(self.pc + 1),
               self.ram_read(self.pc + 2)),
              end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            command = self.ram[self.pc]

            command_string = format(command, '#010b')

            instruction_bits = command_string[2:4]

            if instruction_bits == '10':
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
            elif instruction_bits == '01':
                operand_a = self.ram_read(self.pc + 1)
                operand_b = None
            else:
                operand_a = None
                operand_b = None

   

convert = int('0b00001000', 2)
print(convert)
