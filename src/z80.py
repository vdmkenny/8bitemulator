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
            "Ap": 0x00,
            "Bp": 0x00,
            "Cp": 0x00,
            "Dp": 0x00,
            "Ep": 0x00,
            "Hp": 0x00,
            "Lp": 0x00,
            "Fp": 0x00,
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
            0x08: (self.EX_AF_AFp, 0),
            0x09: (self.ADD_HL_BC, 0),
            0x0A: (self.LD_A_BC, 0),
            0x0B: (self.DEC_BC, 0),
            0x0C: (self.INC_C, 0),
            0x0D: (self.DEC_C, 0),
            0x0E: (self.LD_C_d8, 1),
            0x0F: (self.RRCA, 0),
            0x10: (self.DJNZ, 1),
            0x11: (self.LD_DE_d16, 2),
            0x12: (self.LD_DE_A, 0),
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
            0x20: (self.JR_NZ_d8, 1),
            0x21: (self.LD_HL_d16, 2),
            0x22: (self.LD_d16_HL, 2),
            0x23: (self.INC_HL, 0),
            0x24: (self.INC_H, 0),
            0x25: (self.DEC_H, 0),
            0x26: (self.LD_H_d8, 0),
            0x27: (self.DAA, 0),
            0x28: (self.JR_Z, 1),
            0x29: (self.ADD_HL_HL, 0),
            0x2A: (self.LD_HL_a16, 2),
            0x2B: (self.DEC_HL, 0),
            0x2C: (self.INC_L, 0),
            0x2D: (self.DEC_L, 0),
            0x2E: (self.LD_L_d8, 1),
            0x2F: (self.CPL, 0),
            0x30: (self.JR_NC, 1),
            0x31: (self.LD_SP_d16, 2),
            0x32: (self.LD_a16_A, 2),
            0x33: (self.INC_SP, 0),
            0x34: (self.INC_HL_MEM, 0),
            0x35: (self.DEC_HL_MEM, 0),
            0x36: (self.LD_HL_MEM_d8, 1),
            0x37: (self.SCF, 0),
            0x38: (self.JR_C, 2),
            0x39: (self.ADD_HL_SP, 0),
            0x3A: (self.LD_A_a16, 2),
            0x3B: (self.DEC_SP, 0),
            0x3C: (self.INC_A, 0),
            0x3D: (self.DEC_A, 0),
            0x3E: (self.LD_A_d8, 1),
            0x3F: (self.CCF, 0),
            0x40: (self.LD_B_B, 0),
            0x41: (self.LD_B_C, 0),
            0x42: (self.LD_B_D, 0),
            0x43: (self.LD_B_E, 0),
            0x44: (self.LD_B_H, 0),
            0x45: (self.LD_B_L, 0),
            0x46: (self.LD_B_HL_MEM, 0),
            0x47: (self.LD_B_A, 0),
            0x48: (self.LD_C_B, 0),
            0x49: (self.LD_C_C, 0),
            0x4A: (self.LD_C_D, 0),
            0x4B: (self.LD_C_E, 0),
            0x4C: (self.LD_C_H, 0),
            0x4D: (self.LD_C_L, 0),
            0x4E: (self.LD_C_HL_MEM, 0),
            0x4F: (self.LD_C_A, 0),
            0x50: (self.LD_D_B, 0),
            0x51: (self.LD_D_C, 0),
            0x52: (self.LD_D_D, 0),
            0x53: (self.LD_D_E, 0),
            0x54: (self.LD_D_H, 0),
            0x55: (self.LD_D_L, 0),
            0x56: (self.LD_D_HL_MEM, 0),
            0x57: (self.LD_D_A, 0),
            0x58: (self.LD_E_B, 0),
            0x59: (self.LD_E_C, 0),
            0x5A: (self.LD_E_D, 0),
            0x5B: (self.LD_E_E, 0),
            0x5C: (self.LD_E_H, 0),
            0x5D: (self.LD_E_L, 0),
            0x5E: (self.LD_E_HL_MEM, 0),
            0x5F: (self.LD_E_A, 0),
            0x60: (self.LD_H_B, 0),
            0x61: (self.LD_H_C, 0),
            0x62: (self.LD_H_D, 0),
            0x63: (self.LD_H_E, 0),
            0x64: (self.LD_H_H, 0),
            0x65: (self.LD_H_L, 0),
            0x66: (self.LD_H_HL_MEM, 0),
            0x67: (self.LD_H_A, 0),
            0x68: (self.LD_L_B, 0),
            0x69: (self.LD_L_C, 0),
            0x6A: (self.LD_L_D, 0),
            0x6B: (self.LD_L_E, 0),
            0x6C: (self.LD_L_H, 0),
            0x6D: (self.LD_L_L, 0),
            0x6E: (self.LD_L_HL_MEM, 0),
            0x6F: (self.LD_L_A, 0),
            0x7E: (self.LD_A_HL, 0)
            # TODO: add the rest until 0xFF
        }

    def get_flag(self, flag):
        if flag in self.flags:
            return self.flags[flag]
        else:
            raise ValueError(f"Invalid flag: {register}")

    def set_flag(self, flag, value):
        if flag in self.flags:
            self.flags[flag] = value & 1
        else:
            raise ValueError(f"Invalid flag: {register}")

    def get_register(self, register):
        if register == "AF":
            return (self.registers["A"] << 8) + self.registers["F"]
        elif register == "BC":
            return (self.registers["B"] << 8) + self.registers["C"]
        elif register == "DE":
            return (self.registers["D"] << 8) + self.registers["E"]
        elif register == "HL":
            return (self.registers["H"] << 8) + self.registers["L"]
        elif register == "AFp":
            return (self.registers["Ap"] << 8) + self.registers["Fp"]
        elif register == "BCp":
            return (self.registers["Bp"] << 8) + self.registers["Cp"]
        elif register == "DEp":
            return (self.registers["Dp"] << 8) + self.registers["Ep"]
        elif register == "HLp":
            return (self.registers["Hp"] << 8) + self.registers["Lp"]
        elif register in [
            "A",
            "B",
            "C",
            "D",
            "E",
            "H",
            "L",
            "Ap",
            "Bp",
            "Cp",
            "Dp",
            "Ep",
            "Hp",
            "Lp",
        ]:
            return self.registers[register]
        else:
            raise ValueError(f"Invalid register: {register}")

    def set_register(self, register, value):
        if register in ["AF", "BC", "DE", "HL"]:
            self.registers[register[0]] = value >> 8
            self.registers[register[1]] = value & 0xFF
        elif register in ["AFp", "BCp", "DEp", "HLp"]:
            self.registers[register[0] + "p"] = value >> 8
            self.registers[register[1] + "p"] = value & 0xFF
        elif register in [
            "A",
            "B",
            "C",
            "D",
            "E",
            "H",
            "L",
            "Ap",
            "Bp",
            "Cp",
            "Dp",
            "Ep",
            "Hp",
            "Lp",
        ]:
            self.registers[register] = value
        else:
            raise ValueError(f"Invalid register: {register}")

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

    def increment_memory(self, address):
        value = self.memory_mapper.read_byte(address)
        self.memory_mapper.write_byte(address, (value + 1) & 0xFF)

    def decrement_memory(self, address):
        value = self.memory_mapper.read_byte(address)
        self.memory_mapper.write_byte(address, (value - 1) & 0xFF)

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
                raise ValueError(f"Unknown opcode: {hex(opcode)}")
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

    def EX_AF_AFp(self):
        temp = self.get_register["AFp"]
        self.set_register["AFp"] = self.get_register["AF"]
        self.set_register["AF"] = temp

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
        self.set_register("B", self.get_register("B") - 1)
        if self.get_register("B") != 0:
            self.set_register("PC", self.get_register("PC") + D)

    def LD_DE_d16(self, operand1, operand2):
        self.set_register("DE", (operand2 << 8) | operand1)

    def LD_DE_A(self):
        self.memory_map.write_byte(self.get_register("DE"), self.get_register("A"))

    def INC_DE(self):
        self.increment_register("DE")

    def INC_D(self):
        self.increment_register("D")

    def DEC_D(self):
        self.decrement_register("D")

    def LD_D_d8(self, operand):
        self.set_register("D", operand)

    def JR(self, operand):
        pc = self.get_register("PC")
        offset = operand if operand <= 0x7F else operand - 0x100
        self.set_register("PC", pc + offset)

    def ADD_HL_DE(self):
        result = self.get_register("HL") + self.get_register("DE")
        self.set_flag("H", (result & 0xFFF) < (self.get_register("HL") & 0xFFF))
        self.set_flag("C", result > 0xFFFF)
        self.set_register("HL", result & 0xFFFF)
        self.set_flag("Z", False)
        self.set_flag("N", False)

    def LD_A_DE(self):
        self.set_register("A", self.get_register("DE") & 0xFF)

    def DEC_DE(self):
        self.decrement_register("DE")

    def INC_E(self):
        self.increment_register("E")

    def DEC_E(self):
        self.decrement_register("E")

    def LD_E_d8(self, operand):
        self.set_register("E", operand & 0xFF)

    def RRA(self):
        carry = self.get_flag("C")
        self.set_flag("C", self.A & 1)
        self.set_register("A", ((self.A >> 1) & 0xFF) | (carry << 7))

    def JR_NZ_d8(self, operand):
        if not self.get_flag("Z"):
            pc = self.get_register("PC")
            self.set_register("PC", (pc + operand) & 0xFFFF)

    def LD_HL_d16(self, operand1, operand2):
        self.set_register("HL", (operand2 << 8) | operand1)

    def LD_d16_HL(self, operand1, operand2):
        address = (operand1 << 8) + operand2
        value = self.get_register("HL")
        self.memory_mapper.write_byte(address, value & 0xFF)
        self.memory_mapper.write_byte(address + 1, value >> 8)

    def INC_HL(self):
        self.increment_register("HL")

    def INC_H(self):
        self.increment_register("H")

    def DEC_H(self):
        self.decrement_register("H")

    def LD_H_d8(self, operand):
        self.set_register("H", operand & 0xFF)

    def DAA(self):
        a = self.get_register("A")
        c = self.get_flag("C")
        h = self.get_flag("H")

        if (a & 0x0F) > 9 or h:
            a += 0x06
        if (a & 0xF0) > 0x90 or c:
            a += 0x60
            c = True
        else:
            c = False

        self.set_register("A", a)
        self.set_flag("C", c)
        self.set_flag("H", False)
        self.set_flag("N", False)
        self.set_flag("Z", a == 0)
        self.set_flag("P", False)
        self.set_flag("S", False)

    def JR_Z(self, operand):
        if self.get_flag("Z"):
            self.set_register("PC", self.get_register("PC") + operand)

    def ADD_HL_HL(self):
        result = self.get_register("HL") + self.get_register("HL")
        self.set_register("HL", result & 0xFFFF)

        # Set carry flag if result is greater than 0xFFFF
        if result > 0xFFFF:
            self.set_flag("C", 1)
        else:
            self.set_flag("C", 0)

        # Reset N flag
        self.set_flag("N", 0)

        # Set H flag if carry from bit 11
        if (result & 0x0FFF) > 0x0FFF:
            self.set_flag("H", 1)
        else:
            self.set_flag("H", 0)

        # Reset other flags
        self.set_flag("Z", 0)
        self.set_flag("S", 0)
        self.set_flag("P/V", 0)

    def LD_HL_a16(self, operand1, operand2):
        address = (operand2 << 8) + operand1
        value = self.memory_mapper.read_byte(address)
        self.set_register("L", value & 0xFF)
        value = self.memory_mapper.read_byte(address + 1)
        self.set_register("H", value & 0xFF)

    def DEC_HL(self):
        self.decrement_register("HL")

    def INC_L(self):
        self.increment_register("L")

    def DEC_L(self):
        self.decrement_register("L")

    def LD_L_d8(self, operand):
        self.set_register("L", operand & 0xFF)

    def CPL(self):
        self.registers["A"] = ~self.registers["A"] & 0xFF
        self.set_flag("N", 1)
        self.set_flag("H", 1)

    def JR_NC(self, operand):
        if not self.get_flag("C"):
            pc = self.get_register("PC")
            self.set_register("PC", pc + sign(operand))

    def LD_SP_d16(self, operand1, operand2):
        self.set_register("SP", (operand2 << 8) | operand1)

    def LD_a16_A(self, operand1, operand2):
        address = (operand2 << 8) | operand1
        self.memory_mapper.write_byte(address, self.get_register("A"))

    def INC_SP(self):
        self.increment_register("SP")

    def INC_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        result = self.increment_memory(hl)
        self.set_flag("Z", result == 0)
        self.set_flag("N", False)
        self.set_flag("H", (value & 0x0F) == 0x0F)

    def DEC_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        result = self.decrement_memory(hl)
        self.set_flag("Z", result == 0)
        self.set_flag("N", False)
        self.set_flag("H", (value & 0x0F) == 0x0F)

    def LD_HL_MEM_d8(self, operand):
        hl = self.get_register("HL")
        self.memory_mapper.write_byte(hl, operand)

    def SCF(self):
        self.set_flag("C", True)

    def JR_C(self, operand):
        if self.get_flag("C"):
            self.jump_relative(operand)

    def ADD_HL_SP(self):
        result = self.get_register("HL") + self.get_register("SP")
        self.set_register("HL", result & 0xFFFF)

        # Set carry flag if result is greater than 0xFFFF
        if result > 0xFFFF:
            self.set_flag("C", 1)
        else:
            self.set_flag("C", 0)

        # Reset N flag
        self.set_flag("N", 0)

        # Set H flag if carry from bit 11
        if (result & 0x0FFF) > 0x0FFF:
            self.set_flag("H", 1)
        else:
            self.set_flag("H", 0)

        # Reset other flags
        self.set_flag("Z", 0)
        self.set_flag("S", 0)
        self.set_flag("P/V", 0)

    def LD_A_a16(self, operand1, operand2):
        address = (operand2 << 8) | operand1
        value = self.memory_mapper.read_byte(address) & 0xFF
        self.set_register("A", value)

    def DEC_SP(self):
        self.deccrement_register("SP")

    def INC_A(self):
        self.increment_register("A")

    def DEC_A(self):
        self.decrement_register("A")

    def LD_A_d8(self, operand):
        self.set_register("A", operand & 0xFF)

    def CCF(self):
        self.set_flag("C", ~self.get_flag("C"))
        self.set_flag("N", 0)
        self.set_flag("H", 0)

    def LD_B_B(self):
        value = self.get_register("B")
        self.set_register("B", value)

    def LD_B_C(self):
        value = self.get_register("C")
        self.set_register("B", value)

    def LD_B_D(self):
        value = self.get_register("D")
        self.set_register("B", value)

    def LD_B_E(self):
        value = self.get_register("E")
        self.set_register("B", value)

    def LD_B_H(self):
        value = self.get_register("H")
        self.set_register("B", value)

    def LD_B_L(self):
        value = self.get_register("L")
        self.set_register("B", value)

    def LD_B_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        self.set_register("B", value)

    def LD_B_A(self):
        value = self.get_register("A")
        self.set_register("B", value)

    def LD_C_B(self):
        value = self.get_register("B")
        self.set_register("C", value)

    def LD_C_C(self):
        value = self.get_register("C")
        self.set_register("C", value)

    def LD_C_D(self):
        value = self.get_register("D")
        self.set_register("C", value)

    def LD_C_E(self):
        value = self.get_register("E")
        self.set_register("C", value)

    def LD_C_H(self):
        value = self.get_register("H")
        self.set_register("C", value)

    def LD_C_L(self):
        value = self.get_register("L")
        self.set_register("C", value)

    def LD_C_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        self.set_register("C", value)

    def LD_C_A(self):
        value = self.get_register("A")
        self.set_register("C", value)

    def LD_D_B(self):
        value = self.get_register("B")
        self.set_register("D", value)

    def LD_D_C(self):
        value = self.get_register("C")
        self.set_register("D", value)

    def LD_D_D(self):
        value = self.get_register("D")
        self.set_register("D", value)

    def LD_D_E(self):
        value = self.get_register("E")
        self.set_register("D", value)

    def LD_D_H(self):
        value = self.get_register("H")
        self.set_register("D", value)

    def LD_D_L(self):
        value = self.get_register("L")
        self.set_register("D", value)

    def LD_D_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        self.set_register("D", value)

    def LD_D_A(self):
        value = self.get_register("A")
        self.set_register("D", value)

    def LD_E_B(self):
        value = self.get_register("B")
        self.set_register("E", value)

    def LD_E_C(self):
        value = self.get_register("C")
        self.set_register("E", value)

    def LD_E_D(self):
        value = self.get_register("D")
        self.set_register("E", value)

    def LD_E_E(self):
        value = self.get_register("E")
        self.set_register("E", value)

    def LD_E_H(self):
        value = self.get_register("H")
        self.set_register("E", value)

    def LD_E_L(self):
        value = self.get_register("L")
        self.set_register("E", value)

    def LD_E_HL_MEM(self):
        hl = self.get_register("HL")
        value = self.memory_mapper.read_byte(hl)
        self.set_register("E", value)

    def LD_E_A(self):
        value = self.get_register("A")
        self.set_register("E", value)

    def LD_A_HL(self):
        self.set_register("A", self.get_register("HL") & 0xFF)
