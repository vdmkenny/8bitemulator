class Z80:
    def __init__(self):
        self.A = 0x00
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.H = 0x00
        self.L = 0x00
        self.PC = 0x0000
        self.SP = 0x0000
        self.FLAG_Z = 0x00
        self.FLAG_N = 0x00
        self.FLAG_H = 0x00
        self.FLAG_C = 0x00
        self.memory = bytearray(0x10000)
        self.OPCODES = {
            0x00: (self.nop, 0),
            0x01: (self.ld_bc_nn, 2),
            0x02: (self.ld_bc_a, 0),
            0x03: (self.inc_bc, 0),
            0x05: (self.dec_b, 0),
            0x06: (self.ld_b_n, 1),
            0x21: (self.ld_hl_nn, 2),
            0x22: (self.ld_nn_hl, 2),
            0x2A: (self.ld_hl_nnp, 2),
            0x0A: (self.ld_a_bc, 0),
            0x1A: (self.ld_a_de, 0),
            0x3A: (self.ld_a_nnp, 2)
            # ...
        }

    def decode(self, code):
        # Iterate over the code in 2-byte chunks
        i = 0
        while i < len(code):
            opcode = code[i]
            # Check if the opcode is a prefix
            if opcode == 0xCB:
                opcode = code[i+1]
                i += 1
            if opcode in self.OPCODES:
                func, num_operands = self.OPCODES[opcode]
                operands = []
                for j in range(num_operands):
                    operands.append(code[i+j+1])
                func(*operands)
                i += num_operands + 1
            else:
                # Handle unknown opcode
                pass
        return

    def nop(self):
        pass

    def ld_bc_nn(self, operand1, operand2):
        self.BC = (operand1 << 8) | operand2

    def ld_bc_a(self):
        self.BC = self.A

    def inc_bc(self):
        self.BC += 1

    def dec_b(self):
        self.B -= 1

    def ld_b_n(self, n):
        self.B = n

    def ld_hl_nn(self, operand1, operand2):
        self.HL = (operand1 << 8) | operand2

    def ld_nn_hl(self, operand1, operand2):
        addr = (operand1 << 8) | operand2
        self.memory[addr] = self.HL
