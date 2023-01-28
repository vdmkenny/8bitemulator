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
            0x7E: (self.LD_A_HL, 0)
            # TODO: Implement the rest
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
        if register in ("A", "B", "C", "D", "E", "H", "L"):
            value = self.get_register(register)
            self.set_register(register, value + 1)
        elif register in ("BC", "DE", "HL", "AF"):
            high_register = register[0]
            low_register = register[1]
            value = self.get_register(register)
            self.set_register(register, value + 1)
            self.set_register(high_register, (value + 1) >> 8)
            self.set_register(low_register, (value + 1) & 0xFF)

    def decrement_register(self, register):
        if register in ("A", "B", "C", "D", "E", "H", "L"):
            value = self.get_register(register)
            self.set_register(register, value - 1)
        elif register in ("BC", "DE", "HL", "AF"):
            high_register = register[0]
            low_register = register[1]
            value = self.get_register(register)
            self.set_register(register, value - 1)
            self.set_register(high_register, (value - 1) >> 8)
            self.set_register(low_register, (value - 1) & 0xFF)

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
                print(f"ERROR: Encounteredunknown opcode: {hex(opcode)}")
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

    def LD_A_HL(self):
        address = self.registers["HL"]  # TODO: handle combined 2 byte registers
        self.registers["A"] = self.memory_mapper.read_byte(address)


#            0x0A: (self.LD_A_BC, 0),
#            0x0B: (self.DEC_BC, 0),
#            0x0C: (self.INC_C, 0),
#            0x0D: (self.DEC_C, 0),
#            0x0E: (self.LD_C_d8, 1),
#            0x0F: (self.RRCA, 0),
#            0x7E: (self.LD_A_HL, 0)
