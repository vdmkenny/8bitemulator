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
            0x07: (self.RLCA, 0),
            0x08: (self.LD_a16_SP, 2),
            0x09: (self.ADD_HL_BC, 0),
            0x0A: (self.LD_A_BC, 0),
            0x0B: (self.DEC_BC, 0),
            0x0C: (self.INC_C, 0),
            0x0D: (self.DEC_C, 0),
            0x0E: (self.LD_C_d8, 1),
            0x0F: (self.RRCA, 0),
            0x10: (self.DJNZ, 1),
            0x11: (self.LD_DE_d16, 2),
            0x12: (self.LD_de_A, 0),
            0x13: (self.INC_DE, 0),
            0x14: (self.INC_D, 0),
            0x15: (self.DEC_D, 0),
            0x16: (self.LD_D_d8, 1),
            0x18: (self.JR, 1),
            0x19: (self.ADD_HL_DE, 0),
            0x1A: (self.LD_A_DE, 0),
            0x1B: (self.DEC_DE, 0),
            0x1C: (self.INC_E, 0),
            0x1D: (self.DEC_E, 0),
            0x1E: (self.LD_E_d8, 1),
            0x1F: (self.RRA, 0),
            0x7E: (self.LD_A_HL, 0)
            # TODO: add the rest until 0xFF
        }

    def get_flag(self, flag):
        if flag in self.flags:
            return self.flags[flag]
        else:
            return 0x00

    def set_flag(self, flag, value):
        if flag in self.flags:
            self.flags[flag] = value

    def get_register(self, register):
        if register == "AF":
            return (self.registers["A"] << 8) + self.registers["F"]
        elif register == "BC":
            return (self.registers["B"] << 8) + self.registers["C"]
        elif register == "DE":
            return (self.registers["D"] << 8) + self.registers["E"]
        elif register == "HL":
            return (self.registers["H"] << 8) + self.registers["L"]
        else:
            return self.registers[register]

    def set_register(self, register, value):
        if register in ["AF", "BC", "DE", "HL"]:
            self.registers[register[0]] = value >> 8
            self.registers[register[1]] = value & 0xFF
        else:
            self.registers[register] = value

    def increment_register(self, register):
        if register in ["A", "B", "C", "D", "E", "H", "L"]:
            value = self.get_register(register)
            result = (value + 1) & 0xFF
            self.set_register(register, result)
            self.set_flag("Z", result == 0)
            self.set_flag("N", 0)
            self.set_flag("H", (value & 0xF) + 1 > 0xF)
        elif register in ["BC", "DE", "HL", "SP"]:
            value = self.get_register(register)
            result = (value + 1) & 0xFFFF
            self.set_register(register, result)
        else:
            raise ValueError(f"Invalid register: {register}")

    def decrement_register(self, register):
        if register in ["A", "B", "C", "D", "E", "H", "L"]:
            value = (self.get_register(register) - 1) & 0xFF
            self.set_register(register, value)
            self.set_flag("Z", value == 0)
            self.set_flag("N", 1)
            self.set_flag("H", (self.get_register(register) & 0xF) == 0xF)
        elif register in ["BC", "DE", "HL", "SP"]:
            value = (self.get_register(register) - 1) & 0xFFFF
            self.set_register(register, value)
        else:
            raise ValueError(f"Invalid register: {register}")

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
                print(f"ERROR: Encountered unknown opcode: {hex(opcode)}")
                pass
        return

    def NOP(self):
        pass

    def LD_BC_d16(self, operand1, operand2):
        self.set_register("BC", (operand2 << 8) | operand1)

    def LD_BC_A(self):
        self.set_register("BC", (0x00 << 8) | self.get_register("A"))

    def INC_BC(self):
        self.increment_register("BC")

    def INC_B(self):
        self.increment_register("B")

    def DEC_B(self):
        self.decrement_register("B")

    def LD_B_d8(self, operand):
        self.set_register("B", operand)

    def RLCA(self):
        carry = self.get_flag("C")
        self.set_flag("C", (self.A >> 7) & 1)
        self.set_register("A", ((self.A << 1) & 0xFF) | carry)

    def LD_a16_SP(self, operand1, operand2):
        address = (operand2 << 8) | operand1
        self.memory_mapper.write_byte(address, self.get_register("SP"))

    def ADD_HL_BC(self):
        result = self.get_register("HL") + self.get_register("BC")
        self.set_flag("H", (result & 0xFFF) < (self.get_register("HL") & 0xFFF))
        self.set_flag("C", result > 0xFFFF)
        self.set_register("HL", result & 0xFFFF)
        self.set_flag("Z", False)
        self.set_flag("N", False)

    def LD_A_BC(self):
        self.set_register("A", self.get_register("BC") & 0xFF)

    def DEC_BC(self):
        self.decrement_register("BC")

    def INC_C(self):
        self.increment_register("C")

    def DEC_C(self):
        self.decrement_register("C")

    def LD_C_d8(self, operand):
        self.set_register("C", operand)

    def RRCA(self):
        carry = self.get_flag("C")
        self.set_flag("C", self.A & 1)
        self.set_register("A", ((self.A >> 1) & 0xFF) | (carry << 7))

    def DJNZ(self, D):
        self.set_register(
            "B", self.get_register("B") - 1
        )  # register can't be negative?
        if self.get_register("B") != 0:
            self.set_register("PC", self.get_register("PC") + D)

    def LD_A_HL(self):
        self.set_register("A", self.get_register("HL") & 0xFF)
