import sys


class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8

        self.mar = 0
        self.mdr = 0
        self.pc = 0

        self.reg[7] = 0xF4
        self.running = True
        self.flag = 0b000

        self.ir = ''

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("use: 04-fileio03.py <filename>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as program:
                address = 0
                for line in program:
                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    if len(num) == 0:
                        continue

                    instruction = int(num, 2)

                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

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
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'PUSH':
            self.reg[7] -= 1
            self.ram[self.reg[7]] = self.reg[reg_a]
        elif op == 'POP':
            self.reg[reg_a] = self.ram[self.reg[7]]
            self.reg[7] += 1
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b001
            else:
                self.flag = 0b000
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

    def ram_read(self, address):
        self.mar = address
        self.mdr = self.ram[self.mar]
        return self.mdr

    def ram_write(self, address, data):
        self.mar = address
        self.mdr = data
        self.ram[self.mar] = self.mdr

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

            op_table = {
                '0b10100000': 'ADD',
                '0b10000010': 'LDI',
                '0b01000111': 'PRN',
                '0b00000001': 'HLT',
                '0b10100010': 'MUL',
                '0b01000101': 'PUSH',
                '0b01000110': 'POP',
                '0b01010000': 'CALL',
                '0b00010001': 'RET',
                '0b10100111': 'CMP',
                '0b01010100': 'JMP',
                '0b01010101': 'JEQ',
                '0b01010110': 'JNE',
            }

            instrution_size_table = {
                'ADD': 3,
                'LDI': 3,
                'PRN': 2,
                'HLT': 0,
                'MUL': 3,
                'PUSH': 2,
                'POP': 2,
                'CALL': 2,
                'RET': 0,
                'JMP': 2,
                'CMP': 3,
                'JEQ': 2,
                'JNE': 2,
            }

            instructions_for_setting_the_pc = [
                'CALL', 'RET', 'JMP', 'JEQ', 'JNE'
            ]

            self.ir = op_table[command_string]

            instruction_size = instrution_size_table[self.ir]

            if self.ir in instructions_for_setting_the_pc:
                if self.ir == 'CALL':
                    self.reg[7] = self.pc + 2
                    self.alu('PUSH', 7)
                    self.pc = self.reg[operand_a]
                elif self.ir == 'RET':
                    self.alu('POP', 7)
                    self.pc = self.reg[7]
                elif self.ir == 'JEQ':
                    if self.flag == 0b001:
                        self.ir = 'JMP'
                    else:
                        self.pc += instruction_size
                elif self.ir == 'JNE':
                    if self.flag == 0b000:
                        self.ir = 'JMP'
                    else:
                        self.pc += instruction_size

                if self.ir == 'JMP':
                    self.pc = self.reg[operand_a]
            else:

                self.pc += instruction_size

                self.alu(self.ir, operand_a, operand_b)
