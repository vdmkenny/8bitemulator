from memorymapper import MemoryMapper


class Z80:
    def __init__(self):
        self.registers = {
            "A": 0x00,
            "B": 0x00,
            "C": 0x00,
            "D": 0x00,
            "E": 0x00,
            "H": 0x00,
            "L": 0x00,
            "F": 0x00,
            "I": 0x00,
            "R": 0x00,
            "SP": 0x0000,
            "PC": 0x0000,
            "IX": 0x0000,
            "IY": 0x0000,
        }
        self.flags = {"C": 0, "N": 0, "P/V": 0, "H": 0, "Z": 0, "S": 0}
        self.memory_mapper = MemoryMapper()
        self.OPCODES = {
            0x00: (self.NOP, 0),
            0x01: (self.LD_BC_d16, 2),
            0x02: (self.LD_BC_A, 0),
            0x03: (self.INC_BC, 0),
            0x04: (self.INC_B, 0),
            0x05: (self.DEC_B, 0),
            0x06: (self.LD_B_d8, 1),
            # 0x07: (self.RLCA, 0),
            # 0x08: (self.LD_a16_SP, 2),
            # 0x09: (self.ADD_HL_BC, 0),
            # 0x0A: (self.LD_A_BC, 0),
            # 0x0B: (self.DEC_BC, 0),
            # 0x0C: (self.INC_C, 0),
            # 0x0D: (self.DEC_C, 0),
            # 0x0E: (self.LD_C_d8, 1),
            # 0x0F: (self.RRCA, 0)
            0x7E: (self.LD_A_HL, 0)
            # TODO: Implement the rest
        }

    def decode(self, code):
        # Iterate over the code in 2-byte chunks
        i = 0
        while i < len(code):
            opcode = code[i]
            # Check if the opcode is a prefix
            if opcode == 0xCB:
                opcode = code[i + 1]
                i += 1
            if opcode in self.OPCODES:
                func, num_operands = self.OPCODES[opcode]
                operands = []
                for j in range(num_operands):
                    operands.append(code[i + j + 1])
                func(*operands)
                i += num_operands + 1
            else:
                # Handle unknown opcode
                pass
        return

    def NOP(self):
        pass

    def LD_BC_d16(self, operand1, operand2):
        self.registers["B"] = operand1
        self.registers["C"] = operand2

    def LD_BC_A(self):
        self.memory[self.registers["BC"]] = self.registers["A"]

    def INC_BC(self):
        self.registers["BC"] += 1

    def INC_B(self):
        self.registers["B"] += 1

    def DEC_B(self):
        self.registers["B"] -= 1

    def LD_B_d8(self, operand):
        self.registers["B"] = operand

    def LD_A_HL(self):
        address = self.registers["HL"]  # TODO: handle combined 2 byte registers
        self.registers["A"] = self.memory_mapper.read_byte(address)
