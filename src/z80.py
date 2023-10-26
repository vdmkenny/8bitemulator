from memorymapper import MemoryMapper

import threading
import time


class Z80:
    def __init__(self, speed=100):
        self.cycles = 0
        self.speed = speed
        self.timer_thread = threading.Thread(target=self.timer_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    # Define CPU tick speed
    def timer_loop(self):
        while True:
            time.sleep(1/self.speed)
            self.timer_tick()

    def timer_tick(self):
        self.cycles += 1
        pass

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
            "SP": 0x0000, # Stack Pointer
            "PC": 0x0000, # Program Counter
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
        self.flags = {
            "S": 0    # Sign Flag
            "Z": 0,   # Zero Flag
            "H": 0,   # Half Carry Flag
            "P/V": 0, # Parity/Overflow Flag
            "C": 0,   # Carry Flag 
            "N": 0,   # Add/Sub Flag 
            }
        self.memory_mapper = MemoryMapper()
        self.OPCODES = {
            0x00: (self.NOP),
            0x01: (self.LD, ["BC", "d16"]),
            0x02: (self.LD, ["BC", "A"]),
            0x03: (self.INC, ["BC"]),
            0x04: (self.INC, ["B"]),
            0x05: (self.DEC, ["B"]),
            0x06: (self.LD, ["B", "d8"]),
            0x07: (self.RLCA),
            0x08: (self.EX, ["AF", "AF'"]),
            0x09: (self.ADD, ["HL", "BC"]),
            0x0A: (self.LD, ["A", "BC"]),
            0x0B: (self.DEC, ["BC"]),
            0x0C: (self.INC, ["C"]),
            0x0D: (self.DEC, ["C"]),
            0x0E: (self.LD, ["C", "d8"]),
            0x0F: (self.RRCA),
            0x10: (self.DJNZ, ["r8"]),
            0x11: (self.LD, ["DE", "d16"]),
            0x12: (self.LD, ["DE", "A"]),
            0x13: (self.INC, ["DE"]),
            0x14: (self.INC, ["D"]),
            0x15: (self.DEC, ["D"]),
            0x16: (self.LD, ["D", "d8"]),
            0x17: (self.RLA),
            0x18: (self.JR, ["r8"]),
            0x19: (self.ADD, ["HL", "DE"]),
            0x1A: (self.LD, ["A", "DE"]),
            0x1B: (self.DEC, ["DE"]),
            0x1C: (self.INC, ["E"]),
            0x1D: (self.DEC, ["E"]),
            0x1E: (self.LD, ["E", "d8"]),
            0x1F: (self.RRA),
            0x20: (self.JR, ["NZ", "r8"]),
            0x21: (self.LD, ["HL", "d16"]),
            0x22: (self.LD, ["(d16)", "HL"]),
            0x23: (self.INC, ["HL"]),
            0x24: (self.INC, ["H"]),
            0x25: (self.DEC, ["H"]),
            0x26: (self.LD, ["H", "d8"]),
            0x27: (self.DAA),
            0x28: (self.JR, ["Z", "r8"]),
            0x29: (self.ADD, ["HL", "HL"]),
            0x2A: (self.LD, ["HL", "(d16)"]),
            0x2B: (self.DEC, ["HL"]),
            0x2C: (self.INC, ["L"]),
            0x2D: (self.DEC, ["L"]),
            0x2E: (self.LD, ["L", "d8"]),
            0x2F: (self.CPL),
            0x30: (self.JR, ["NC", "r8"]),
            0x31: (self.LD, ["SP", "d16"]),
            0x32: (self.LD, ["(d16)", "A"]),
            0x33: (self.INC, ["SP"]),
            0x34: (self.INC, ["(HL)"]),
            0x35: (self.DEC, ["(HL)"]),
            0x36: (self.LD, ["(HL)", "d8"]),
            0x37: (self.SCF),
            0x38: (self.JR, ["C", "r8"]),
            0x39: (self.ADD, ["HL", "SP"]),
            0x3A: (self.LD, ["A", "(d16)"]),
            0x3B: (self.DEC, ["SP"]),
            0x3C: (self.INC, ["A"]),
            0x3D: (self.DEC, ["A"]),
            0x3E: (self.LD, ["A", "d8"]),
            0x3F: (self.CCF),
            0x40: (self.LD, ["B", "B"]),
            0x41: (self.LD, ["B", "C"]),
            0x42: (self.LD, ["B", "D"]),
            0x43: (self.LD, ["B", "E"]),
            0x44: (self.LD, ["B", "H"]),
            0x45: (self.LD, ["B", "L"]),
            0x46: (self.LD, ["B", "(HL)"]),
            0x47: (self.LD, ["B", "A"]),
            0x48: (self.LD, ["C", "B"]),
            0x49: (self.LD, ["C", "C"]),
            0x4A: (self.LD, ["C", "D"]),
            0x4B: (self.LD, ["C", "E"]),
            0x4C: (self.LD, ["C", "H"]),
            0x4D: (self.LD, ["C", "L"]),
            0x4E: (self.LD, ["C", "(HL)"]),
            0x4F: (self.LD, ["C", "A"]),
            0x50: (self.LD, ["D", "B"]),
            0x51: (self.LD, ["D", "C"]),
            0x52: (self.LD, ["D", "D"]),
            0x53: (self.LD, ["D", "E"]),
            0x54: (self.LD, ["D", "H"]),
            0x55: (self.LD, ["D", "L"]),
            0x56: (self.LD, ["D", "(HL)"]),
            0x57: (self.LD, ["D", "A"]),
            0x58: (self.LD, ["E", "B"]),
            0x59: (self.LD, ["E", "C"]),
            0x5A: (self.LD, ["E", "D"]),
            0x5B: (self.LD, ["E", "E"]),
            0x5C: (self.LD, ["E", "H"]),
            0x5D: (self.LD, ["E", "L"]),
            0x5E: (self.LD, ["E", "(HL)"]),
            0x5F: (self.LD, ["E", "A"]),
            0x60: (self.LD, ["H", "B"]),
            0x61: (self.LD, ["H", "C"]),
            0x62: (self.LD, ["H", "D"]),
            0x63: (self.LD, ["H", "E"]),
            0x64: (self.LD, ["H", "H"]),
            0x65: (self.LD, ["H", "L"]),
            0x66: (self.LD, ["H", "(HL)"]),
            0x67: (self.LD, ["H", "A"]),
            0x68: (self.LD, ["L", "B"]),
            0x69: (self.LD, ["L", "C"]),
            0x6A: (self.LD, ["L", "D"]),
            0x6B: (self.LD, ["L", "E"]),
            0x6C: (self.LD, ["L", "H"]),
            0x6D: (self.LD, ["L", "L"]),
            0x6E: (self.LD, ["L", "(HL)"]),
            0x6F: (self.LD, ["L", "A"]),
            0x70: (self.LD, ["(HL)", "B"]),
            0x71: (self.LD, ["(HL)", "C"]),
            0x72: (self.LD, ["(HL)", "D"]),
            0x73: (self.LD, ["(HL)", "E"]),
            0x74: (self.LD, ["(HL)", "H"]),
            0x75: (self.LD, ["(HL)", "L"]),
            0x76: (self.HALT),
            0x77: (self.LD, ["(HL)", "A"]),
            0x78: (self.LD, ["A", "B"]),
            0x79: (self.LD, ["A", "C"]),
            0x7A: (self.LD, ["A", "D"]),
            0x7B: (self.LD, ["A", "E"]),
            0x7C: (self.LD, ["A", "H"]),
            0x7D: (self.LD, ["A", "L"]),
            0x7E: (self.LD, ["A", "(HL)"]),
            0x7F: (self.LD, ["A", "A"]),
            0x80: (self.ADD, ["A", "B"]),
            0x81: (self.ADD, ["A", "C"]),
            0x82: (self.ADD, ["A", "D"]),
            0x83: (self.ADD, ["A", "E"]),
            0x84: (self.ADD, ["A", "H"]),
            0x85: (self.ADD, ["A", "L"]),
            0x86: (self.ADD, ["A", "(HL)"]),
            0x87: (self.ADD, ["A", "A"]),
            0x88: (self.ADC, ["A", "B"]),
            0x89: (self.ADC, ["A", "C"]),
            0x8A: (self.ADC, ["A", "D"]),
            0x8B: (self.ADC, ["A", "E"]),
            0x8C: (self.ADC, ["A", "H"]),
            0x8D: (self.ADC, ["A", "L"]),
            0x8E: (self.ADC, ["A", "(HL)"]),
            0x8F: (self.ADC, ["A", "A"]),
            0x90: (self.SUB, ["A", "B"]),
            0x91: (self.SUB, ["A", "C"]),
            0x92: (self.SUB, ["A", "D"]),
            0x93: (self.SUB, ["A", "E"]),
            0x94: (self.SUB, ["A", "H"]),
            0x95: (self.SUB, ["A", "L"]),
            0x96: (self.SUB, ["A", "(HL)"]),
            0x97: (self.SUB, ["A", "A"]),
            0x98: (self.SBC, ["A", "B"]),
            0x99: (self.SBC, ["A", "C"]),
            0x9A: (self.SBC, ["A", "D"]),
            0x9B: (self.SBC, ["A", "E"]),
            0x9C: (self.SBC, ["A", "H"]),
            0x9D: (self.SBC, ["A", "L"]),
            0x9E: (self.SBC, ["A", "(HL)"]),
            0x9F: (self.SBC, ["A", "A"]),
            0xA0: (self.AND, ["A", "B"]),
            0xA1: (self.AND, ["A", "C"]),
            0xA2: (self.AND, ["A", "D"]),
            0xA3: (self.AND, ["A", "E"]),
            0xA4: (self.AND, ["A", "H"]),
            0xA5: (self.AND, ["A", "L"]),
            0xA6: (self.AND, ["A", "(HL)"]),
            0xA7: (self.AND, ["A", "A"]),
            0xA8: (self.XOR, ["A", "B"]),
            0xA9: (self.XOR, ["A", "C"]),
            0xAA: (self.XOR, ["A", "D"]),
            0xAB: (self.XOR, ["A", "E"]),
            0xAC: (self.XOR, ["A", "H"]),
            0xAD: (self.XOR, ["A", "L"]),
            0xAE: (self.XOR, ["A", "(HL)"]),
            0xAF: (self.XOR, ["A", "A"]),
            0xB0: (self.OR, ["A", "B"]),
            0xB1: (self.OR, ["A", "C"]),
            0xB2: (self.OR, ["A", "D"]),
            0xB3: (self.OR, ["A", "E"]),
            0xB4: (self.OR, ["A", "H"]),
            0xB5: (self.OR, ["A", "L"]),
            0xB6: (self.OR, ["A", "(HL)"]),
            0xB7: (self.OR, ["A", "A"]),
            0xB8: (self.CP, ["A", "B"]),
            0xB9: (self.CP, ["A", "C"]),
            0xBA: (self.CP, ["A", "D"]),
            0xBB: (self.CP, ["A", "E"]),
            0xBC: (self.CP, ["A", "H"]),
            0xBD: (self.CP, ["A", "L"]),
            0xBE: (self.CP, ["A", "(HL)"]),
            0xBF: (self.CP, ["A", "A"]),
            0xC0: (self.RET_NZ,),
            0xC1: (self.POP, ["BC"]),
            0xC2: (self.JP_NZ,),
            0xC3: (self.JP,),
            0xC4: (self.CALL_NZ,),
            0xC5: (self.PUSH, ["BC"]),
            0xC6: (self.ADD, ["A", "d8"]),
            0xC7: (self.RST, [0x00]),
            0xC8: (self.RET_Z,),
            0xC9: (self.RET,),
            0xCA: (self.JP_Z,),
            0xCB: (self.CB,),
            0xCC: (self.CALL_Z,),
            0xCD: (self.CALL,),
            0xCE: (self.ADC, ["A", "d8"]),
            0xCF: (self.RST, [0x08]),
            0xD0: (self.RET_NC,),
            0xD1: (self.POP, ["DE"]),
            0xD2: (self.JP_NC,),
            0xD3: (self.OUT, ["(a8)", "A"]),
            0xD4: (self.CALL_NC,),
            0xD5: (self.PUSH, ["DE"]),
            0xD6: (self.SUB, ["A", "d8"]),
            0xD7: (self.RST, [0x10]),
            0xD8: (self.RET_C,),
            0xD9: (self.RETI,),
            0xDA: (self.JP_C,),
            0xDB: (self.IN, ["A", "(a8)"]),
            0xDC: (self.CALL_C,),
            0xDE: (self.SBC, ["A", "d8"]),
            0xDF: (self.RST, [0x18]),
            0xE0: (self.LDH, ["(a8)", "A"]),
            0xE1: (self.POP, ["HL"]),
            0xE2: (self.LD, ["(C)", "A"]),
            0xE5: (self.PUSH, ["HL"]),
            0xE6: (self.AND, ["A", "d8"]),
            0xE7: (self.RST, [0x20]),
            0xE8: (self.ADD_SP_r8,),
            0xE9: (self.JP_HL,),
            0xEA: (self.LD, ["(a16)", "A"]),
            0xEE: (self.XOR, ["A", "d8"]),
            0xEF: (self.RST, [0x28]),
            0xF0: (self.LDH, ["A", "(a8)"]),
            0xF1: (self.POP, ["AF"]),
            0xF2: (self.LD, ["A", "(C)"]),
            0xF3: (self.DI,),
            0xF5: (self.PUSH, ["AF"]),
            0xF6: (self.OR, ["A", "d8"]),
            0xF7: (self.RST, [0x30]),
            0xF8: (self.LDHL, ["SP", "r8"]),
            0xF9: (self.LD, ["SP", "HL"]),
            0xFA: (self.LD, ["A", "(a16)"]),
            0xFB: (self.EI,),
            0xFE: (self.CP, ["A", "d8"]),
            0xFF: (self.RST, [0x38]),
        }
        self.OPCODES_CB = {
            0x00: (self.RLC, ["B"]),
            0x01: (self.RLC, ["C"]),
            0x02: (self.RLC, ["D"]),
            0x03: (self.RLC, ["E"]),
            0x04: (self.RLC, ["H"]),
            0x05: (self.RLC, ["L"]),
            0x06: (self.RLC, ["(HL)"]),
            0x07: (self.RLC, ["A"]),
            0x08: (self.RRC, ["B"]),
            0x09: (self.RRC, ["C"]),
            0x0A: (self.RRC, ["D"]),
            0x0B: (self.RRC, ["E"]),
            0x0C: (self.RRC, ["H"]),
            0x0D: (self.RRC, ["L"]),
            0x0E: (self.RRC, ["(HL)"]),
            0x0F: (self.RRC, ["A"]),
            0x10: (self.RL, ["B"]),
            0x11: (self.RL, ["C"]),
            0x12: (self.RL, ["D"]),
            0x13: (self.RL, ["E"]),
            0x14: (self.RL, ["H"]),
            0x15: (self.RL, ["L"]),
            0x16: (self.RL, ["(HL)"]),
            0x17: (self.RL, ["A"]),
            0x18: (self.RR, ["B"]),
            0x19: (self.RR, ["C"]),
            0x1A: (self.RR, ["D"]),
            0x1B: (self.RR, ["E"]),
            0x1C: (self.RR, ["H"]),
            0x1D: (self.RR, ["L"]),
            0x1E: (self.RR, ["(HL)"]),
            0x1F: (self.RR, ["A"]),
            0x20: (self.SLA, ["B"]),
            0x21: (self.SLA, ["C"]),
            0x22: (self.SLA, ["D"]),
            0x23: (self.SLA, ["E"]),
            0x24: (self.SLA, ["H"]),
            0x25: (self.SLA, ["L"]),
            0x26: (self.SLA, ["(HL)"]),
            0x27: (self.SLA, ["A"]),
            0x28: (self.SRA, ["B"]),
            0x29: (self.SRA, ["C"]),
            0x2A: (self.SRA, ["D"]),
            0x2B: (self.SRA, ["E"]),
            0x2C: (self.SRA, ["H"]),
            0x2D: (self.SRA, ["L"]),
            0x2E: (self.SRA, ["(HL)"]),
            0x2F: (self.SRA, ["A"]),
            0x30: (self.SLL, ["B"]),
            0x31: (self.SLL, ["C"]),
            0x32: (self.SLL, ["D"]),
            0x33: (self.SLL, ["E"]),
            0x34: (self.SLL, ["H"]),
            0x35: (self.SLL, ["L"]),
            0x36: (self.SLL, ["(HL)"]),
            0x37: (self.SLL, ["A"]),
            0x38: (self.SRL, ["B"]),
            0x39: (self.SRL, ["C"]),
            0x3A: (self.SRL, ["D"]),
            0x3B: (self.SRL, ["E"]),
            0x3C: (self.SRL, ["H"]),
            0x3D: (self.SRL, ["L"]),
            0x3E: (self.SRL, ["(HL)"]),
            0x3F: (self.SRL, ["A"]),
            0x40: (self.BIT, [0, "B"]),
            0x41: (self.BIT, [0, "C"]),
            0x42: (self.BIT, [0, "D"]),
            0x43: (self.BIT, [0, "E"]),
            0x44: (self.BIT, [0, "H"]),
            0x45: (self.BIT, [0, "L"]),
            0x46: (self.BIT, [0, "(HL)"]),
            0x47: (self.BIT, [0, "A"]),
            0x48: (self.BIT, [1, "B"]),
            0x49: (self.BIT, [1, "C"]),
            0x4A: (self.BIT, [1, "D"]),
            0x4B: (self.BIT, [1, "E"]),
            0x4C: (self.BIT, [1, "H"]),
            0x4D: (self.BIT, [1, "L"]),
            0x4E: (self.BIT, [1, "(HL)"]),
            0x4F: (self.BIT, [1, "A"]),
            0x50: (self.BIT, [2, "B"]),
            0x51: (self.BIT, [2, "C"]),
            0x52: (self.BIT, [2, "D"]),
            0x53: (self.BIT, [2, "E"]),
            0x54: (self.BIT, [2, "H"]),
            0x55: (self.BIT, [2, "L"]),
            0x56: (self.BIT, [2, "(HL)"]),
            0x57: (self.BIT, [2, "A"]),
            0x58: (self.BIT, [3, "B"]),
            0x59: (self.BIT, [3, "C"]),
            0x5A: (self.BIT, [3, "D"]),
            0x5B: (self.BIT, [3, "E"]),
            0x5C: (self.BIT, [3, "H"]),
            0x5D: (self.BIT, [3, "L"]),
            0x5E: (self.BIT, [3, "(HL)"]),
            0x5F: (self.BIT, [3, "A"]),
            0x60: (self.BIT, [4, "B"]),
            0x61: (self.BIT, [4, "C"]),
            0x62: (self.BIT, [4, "D"]),
            0x63: (self.BIT, [4, "E"]),
            0x64: (self.BIT, [4, "H"]),
            0x65: (self.BIT, [4, "L"]),
            0x66: (self.BIT, [4, "(HL)"]),
            0x67: (self.BIT, [4, "A"]),
            0x68: (self.BIT, [5, "B"]),
            0x69: (self.BIT, [5, "C"]),
            0x6A: (self.BIT, [5, "D"]),
            0x6B: (self.BIT, [5, "E"]),
            0x6C: (self.BIT, [5, "H"]),
            0x6D: (self.BIT, [5, "L"]),
            0x6E: (self.BIT, [5, "(HL)"]),
            0x6F: (self.BIT, [5, "A"]),
            0x70: (self.BIT, [6, "B"]),
            0x71: (self.BIT, [6, "C"]),
            0x72: (self.BIT, [6, "D"]),
            0x73: (self.BIT, [6, "E"]),
            0x74: (self.BIT, [6, "H"]),
            0x75: (self.BIT, [6, "L"]),
            0x76: (self.BIT, [6, "(HL)"]),
            0x77: (self.BIT, [6, "A"]),
            0x78: (self.BIT, [7, "B"]),
            0x79: (self.BIT, [7, "C"]),
            0x7A: (self.BIT, [7, "D"]),
            0x7B: (self.BIT, [7, "E"]),
            0x7C: (self.BIT, [7, "H"]),
            0x7D: (self.BIT, [7, "L"]),
            0x7E: (self.BIT, [7, "(HL)"]),
            0x7F: (self.BIT, [7, "A"]),
            0x80: (self.RES, [0, "B"]),
            0x81: (self.RES, [0, "C"]),
            0x82: (self.RES, [0, "D"]),
            0x83: (self.RES, [0, "E"]),
            0x84: (self.RES, [0, "H"]),
            0x85: (self.RES, [0, "L"]),
            0x86: (self.RES, [0, "(HL)"]),
            0x87: (self.RES, [0, "A"]),
            0x88: (self.RES, [1, "B"]),
            0x89: (self.RES, [1, "C"]),
            0x8A: (self.RES, [1, "D"]),
            0x8B: (self.RES, [1, "E"]),
            0x8C: (self.RES, [1, "H"]),
            0x8D: (self.RES, [1, "L"]),
            0x8E: (self.RES, [1, "(HL)"]),
            0x8F: (self.RES, [1, "A"]),
            0x90: (self.RES, [2, "B"]),
            0x91: (self.RES, [2, "C"]),
            0x92: (self.RES, [2, "D"]),
            0x93: (self.RES, [2, "E"]),
            0x94: (self.RES, [2, "H"]),
            0x95: (self.RES, [2, "L"]),
            0x96: (self.RES, [2, "(HL)"]),
            0x97: (self.RES, [2, "A"]),
            0x98: (self.RES, [3, "B"]),
            0x99: (self.RES, [3, "C"]),
            0x9A: (self.RES, [3, "D"]),
            0x9B: (self.RES, [3, "E"]),
            0x9C: (self.RES, [3, "H"]),
            0x9D: (self.RES, [3, "L"]),
            0x9E: (self.RES, [3, "(HL)"]),
            0x9F: (self.RES, [3, "A"]),
            0xA0: (self.RES, [4, "B"]),
            0xA1: (self.RES, [4, "C"]),
            0xA2: (self.RES, [4, "D"]),
            0xA3: (self.RES, [4, "E"]),
            0xA4: (self.RES, [4, "H"]),
            0xA5: (self.RES, [4, "L"]),
            0xA6: (self.RES, [4, "(HL)"]),
            0xA7: (self.RES, [4, "A"]),
            0xA8: (self.RES, [5, "B"]),
            0xA9: (self.RES, [5, "C"]),
            0xAA: (self.RES, [5, "D"]),
            0xAB: (self.RES, [5, "E"]),
            0xAC: (self.RES, [5, "H"]),
            0xAD: (self.RES, [5, "L"]),
            0xAE: (self.RES, [5, "(HL)"]),
            0xAF: (self.RES, [5, "A"]),
            0xB0: (self.RES, [6, "B"]),
            0xB1: (self.RES, [6, "C"]),
            0xB2: (self.RES, [6, "D"]),
            0xB3: (self.RES, [6, "E"]),
            0xB4: (self.RES, [6, "H"]),
            0xB5: (self.RES, [6, "L"]),
            0xB6: (self.RES, [6, "(HL)"]),
            0xB7: (self.RES, [6, "A"]),
            0xB8: (self.RES, [7, "B"]),
            0xB9: (self.RES, [7, "C"]),
            0xBA: (self.RES, [7, "D"]),
            0xBB: (self.RES, [7, "E"]),
            0xBC: (self.RES, [7, "H"]),
            0xBD: (self.RES, [7, "L"]),
            0xBE: (self.RES, [7, "(HL)"]),
            0xBF: (self.RES, [7, "A"]),
            0xC0: (self.SET, [0, "B"]),
            0xC1: (self.SET, [0, "C"]),
            0xC2: (self.SET, [0, "D"]),
            0xC3: (self.SET, [0, "E"]),
            0xC4: (self.SET, [0, "H"]),
            0xC5: (self.SET, [0, "L"]),
            0xC6: (self.SET, [0, "(HL)"]),
            0xC7: (self.SET, [0, "A"]),
            0xC8: (self.SET, [1, "B"]),
            0xC9: (self.SET, [1, "C"]),
            0xCA: (self.SET, [1, "D"]),
            0xCB: (self.SET, [1, "E"]),
            0xCC: (self.SET, [1, "H"]),
            0xCD: (self.SET, [1, "L"]),
            0xCE: (self.SET, [1, "(HL)"]),
            0xCF: (self.SET, [1, "A"]),
            0xD0: (self.SET, [2, "B"]),
            0xD1: (self.SET, [2, "C"]),
            0xD2: (self.SET, [2, "D"]),
            0xD3: (self.SET, [2, "E"]),
            0xD4: (self.SET, [2, "H"]),
            0xD5: (self.SET, [2, "L"]),
            0xD6: (self.SET, [2, "(HL)"]),
            0xD7: (self.SET, [2, "A"]),
            0xD8: (self.SET, [3, "B"]),
            0xD9: (self.SET, [3, "C"]),
            0xDA: (self.SET, [3, "D"]),
            0xDB: (self.SET, [3, "E"]),
            0xDC: (self.SET, [3, "H"]),
            0xDD: (self.SET, [3, "L"]),
            0xDE: (self.SET, [3, "(HL)"]),
            0xDF: (self.SET, [3, "A"]),
            0xE0: (self.SET, [4, "B"]),
            0xE1: (self.SET, [4, "C"]),
            0xE2: (self.SET, [4, "D"]),
            0xE3: (self.SET, [4, "E"]),
            0xE4: (self.SET, [4, "H"]),
            0xE5: (self.SET, [4, "L"]),
            0xE6: (self.SET, [4, "(HL)"]),
            0xE7: (self.SET, [4, "A"]),
            0xE8: (self.SET, [5, "B"]),
            0xE9: (self.SET, [5, "C"]),
            0xEA: (self.SET, [5, "D"]),
            0xEB: (self.SET, [5, "E"]),
            0xEC: (self.SET, [5, "H"]),
            0xED: (self.SET, [5, "L"]),
            0xEE: (self.SET, [5, "(HL)"]),
            0xEF: (self.SET, [5, "A"]),
            0xF0: (self.SET, [6, "B"]),
            0xF1: (self.SET, [6, "C"]),
            0xF2: (self.SET, [6, "D"]),
            0xF3: (self.SET, [6, "E"]),
            0xF4: (self.SET, [6, "H"]),
            0xF5: (self.SET, [6, "L"]),
            0xF6: (self.SET, [6, "(HL)"]),
            0xF7: (self.SET, [6, "A"]),
            0xF8: (self.SET, [7, "B"]),
            0xF9: (self.SET, [7, "C"]),
            0xFA: (self.SET, [7, "D"]),
            0xFB: (self.SET, [7, "E"]),
            0xFC: (self.SET, [7, "H"]),
            0xFD: (self.SET, [7, "L"]),
            0xFE: (self.SET, [7, "(HL)"]),
            0xFF: (self.SET, [7, "A"]),
        }
        self.OPCODES_DD = {
            0x00: None,
            0x01: None,
            0x02: None,
            0x03: None,
            0x04: (self.INC, ["B"]),
            0x05: (self.DEC, ["B"]),
            0x06: (self.LD, ["B", "d8"]),
            0x07: (self.RLC, ["A"]),
            0x08: None,
            0x09: (self.ADD, ["IX", "BC"]),
            0x0A: (self.LD, ["A", "(BC)"]),
            0x0B: None,
            0x0C: (self.INC, ["C"]),
            0x0D: (self.DEC, ["C"]),
            0x0E: (self.LD, ["C", "d8"]),
            0x0F: (self.RRC, ["A"]),
            0x10: None,
            0x11: (self.LD, ["DE", "d16"]),
            0x12: (self.LD, ["(DE)", "A"]),
            0x13: None,
            0x14: (self.INC, ["D"]),
            0x15: (self.DEC, ["D"]),
            0x16: (self.LD, ["D", "d8"]),
            0x17: (self.RL, ["A"]),
            0x18: (self.JR, ["d8"]),
            0x19: (self.ADD, ["IX", "DE"]),
            0x1A: (self.LD, ["A", "(DE)"]),
            0x1B: None,
            0x1C: (self.INC, ["E"]),
            0x1D: (self.DEC, ["E"]),
            0x1E: (self.LD, ["E", "d8"]),
            0x1F: (self.RR, ["A"]),
            0x20: None,
            0x21: (self.LD, ["IX", "d16"]),
            0x22: (self.LD, ["(d16)", "IX"]),
            0x23: None,
            0x24: (self.INC, ["IXH"]),
            0x25: (self.DEC, ["IXH"]),
            0x26: (self.LD, ["IXH", "d8"]),
            0x27: None,
            0x28: (self.JR, ["Z", "d8"]),
            0x29: (self.ADD, ["IX", "IX"]),
            0x2A: (self.LD, ["IX", "(d16)"]),
            0x2B: None,
            0x2C: (self.INC, ["IXL"]),
            0x2D: (self.DEC, ["IXL"]),
            0x2E: (self.LD, ["IXL", "d8"]),
            0x2F: None,
            0x30: (self.JR, ["NC", "d8"]),
            0x31: (self.LD, ["SP", "d16"]),
            0x32: (self.LD, ["(d16)", "A"]),
            0x33: None,
            0x34: (self.INC, ["(IX+d8)"]),
            0x35: (self.DEC, ["(IX+d8)"]),
            0x36: (self.LD, ["(IX+d8)", "d8"]),
            0x37: None,
            0x38: (self.JR, ["C", "d8"]),
            0x39: (self.ADD, ["IX", "SP"]),
            0x3A: (self.LD, ["A", "(d16)"]),
            0x3B: None,
            0x3C: (self.INC, ["A"]),
            0x3D: (self.DEC, ["A"]),
            0x3E: (self.LD, ["A", "d8"]),
            0x3F: None,
            0x40: (self.LD, ["B", "B"]),
            0x41: (self.LD, ["B", "C"]),
            0x42: (self.LD, ["B", "D"]),
            0x43: (self.LD, ["B", "E"]),
            0x44: (self.LD, ["B", "IXH"]),
            0x45: (self.LD, ["B", "IXL"]),
            0x46: (self.LD, ["B", "(IX+d8)"]),
            0x47: (self.LD, ["B", "A"]),
            0x48: (self.LD, ["C", "B"]),
            0x49: (self.LD, ["C", "C"]),
            0x4A: (self.LD, ["C", "D"]),
            0x4B: (self.LD, ["C", "E"]),
            0x4C: (self.LD, ["C", "IXH"]),
            0x4D: (self.LD, ["C", "IXL"]),
            0x4E: (self.LD, ["C", "(IX+d8)"]),
            0x4F: (self.LD, ["C", "A"]),
            0x50: (self.LD, ["D", "B"]),
            0x51: (self.LD, ["D", "C"]),
            0x52: (self.LD, ["D", "D"]),
            0x53: (self.LD, ["D", "E"]),
            0x54: (self.LD, ["D", "IXH"]),
            0x55: (self.LD, ["D", "IXL"]),
            0x56: (self.LD, ["D", "(IX+d8)"]),
            0x57: (self.LD, ["D", "A"]),
            0x58: (self.LD, ["E", "B"]),
            0x59: (self.LD, ["E", "C"]),
            0x5A: (self.LD, ["E", "D"]),
            0x5B: (self.LD, ["E", "E"]),
            0x5C: (self.LD, ["E", "IXH"]),
            0x5D: (self.LD, ["E", "IXL"]),
            0x5E: (self.LD, ["E", "(IX+d8)"]),
            0x5F: (self.LD, ["E", "A"]),
            0x60: (self.LD, ["IXH", "B"]),
            0x61: (self.LD, ["IXH", "C"]),
            0x62: (self.LD, ["IXH", "D"]),
            0x63: (self.LD, ["IXH", "E"]),
            0x64: (self.LD, ["IXH", "IXH"]),
            0x65: (self.LD, ["IXH", "IXL"]),
            0x66: (self.LD, ["H", "(IX+d8)"]),
            0x67: (self.LD, ["IXH", "A"]),
            0x68: (self.LD, ["IXL", "B"]),
            0x69: (self.LD, ["IXL", "C"]),
            0x6A: (self.LD, ["IXL", "D"]),
            0x6B: (self.LD, ["IXL", "E"]),
            0x6C: (self.LD, ["IXL", "IXH"]),
            0x6D: (self.LD, ["IXL", "IXL"]),
            0x6E: (self.LD, ["L", "(IX+d8)"]),
            0x6F: (self.LD, ["IXL", "A"]),
            0x70: (self.LD, ["(IX+d8)", "B"]),
            0x71: (self.LD, ["(IX+d8)", "C"]),
            0x72: (self.LD, ["(IX+d8)", "D"]),
            0x73: (self.LD, ["(IX+d8)", "E"]),
            0x74: (self.LD, ["(IX+d8)", "H"]),
            0x75: (self.LD, ["(IX+d8)", "L"]),
            0x76: (self.HALT),
            0x77: (self.LD, ["(IX+d8)", "A"]),
            0x78: (self.LD, ["A", "B"]),
            0x79: (self.LD, ["A", "C"]),
            0x7A: (self.LD, ["A", "D"]),
            0x7B: (self.LD, ["A", "E"]),
            0x7C: (self.LD, ["A", "IXH"]),
            0x7D: (self.LD, ["A", "IXL"]),
            0x7E: (self.LD, ["A", "(IX+d8)"]),
            0x7F: (self.LD, ["A", "A"]),
            0x80: (self.ADD, ["A", "B"]),
            0x81: (self.ADD, ["A", "C"]),
            0x82: (self.ADD, ["A", "D"]),
            0x83: (self.ADD, ["A", "E"]),
            0x84: (self.ADD, ["A", "IXH"]),
            0x85: (self.ADD, ["A", "IXL"]),
            0x86: (self.ADD, ["A", "(IX+d8)"]),
            0x87: (self.ADD, ["A", "A"]),
            0x88: (self.ADC, ["A", "B"]),
            0x89: (self.ADC, ["A", "C"]),
            0x8A: (self.ADC, ["A", "D"]),
            0x8B: (self.ADC, ["A", "E"]),
            0x8C: (self.ADC, ["A", "IXH"]),
            0x8D: (self.ADC, ["A", "IXL"]),
            0x8E: (self.ADC, ["A", "(IX+d8)"]),
            0x8F: (self.ADC, ["A", "A"]),
            0x90: (self.SUB, ["B"]),
            0x91: (self.SUB, ["C"]),
            0x92: (self.SUB, ["D"]),
            0x93: (self.SUB, ["E"]),
            0x94: (self.SUB, ["IXH"]),
            0x95: (self.SUB, ["IXL"]),
            0x96: (self.SUB, ["(IX+d8)"]),
            0x97: (self.SUB, ["A"]),
            0x98: (self.SBC, ["A", "B"]),
            0x99: (self.SBC, ["A", "C"]),
            0x9A: (self.SBC, ["A", "D"]),
            0x9B: (self.SBC, ["A", "E"]),
            0x9C: (self.SBC, ["A", "IXH"]),
            0x9D: (self.SBC, ["A", "IXL"]),
            0x9E: (self.SBC, ["A", "(IX+d8)"]),
            0x9F: (self.SBC, ["A", "A"]),
            0xA0: (self.AND, ["B"]),
            0xA1: (self.AND, ["C"]),
            0xA2: (self.AND, ["D"]),
            0xA3: (self.AND, ["E"]),
            0xA4: (self.AND, ["IXH"]),
            0xA5: (self.AND, ["IXL"]),
            0xA6: (self.AND, ["(IX+d8)"]),
            0xA7: (self.AND, ["A"]),
            0xA8: (self.XOR, ["B"]),
            0xA9: (self.XOR, ["C"]),
            0xAA: (self.XOR, ["D"]),
            0xAB: (self.XOR, ["E"]),
            0xAC: (self.XOR, ["IXH"]),
            0xAD: (self.XOR, ["IXL"]),
            0xAE: (self.XOR, ["(IX+d8)"]),
            0xAF: (self.XOR, ["A"]),
            0xB0: (self.OR, ["B"]),
            0xB1: (self.OR, ["C"]),
            0xB2: (self.OR, ["D"]),
            0xB3: (self.OR, ["E"]),
            0xB4: (self.OR, ["IXH"]),
            0xB5: (self.OR, ["IXL"]),
            0xB6: (self.OR, ["(IX+d8)"]),
            0xB7: (self.OR, ["A"]),
            0xB8: (self.CP, ["B"]),
            0xB9: (self.CP, ["C"]),
            0xBA: (self.CP, ["D"]),
            0xBB: (self.CP, ["E"]),
            0xBC: (self.CP, ["IXH"]),
            0xBD: (self.CP, ["IXL"]),
            0xBE: (self.CP, ["(IX+d8)"]),
            0xBF: (self.CP, ["A"]),
            0xC0: None,
            0xC1: None,
            0xC2: None,
            0xC3: None,
            0xC4: None,
            0xC5: None,
            0xC6: None,
            0xC7: None,
            0xC8: None,
            0xC9: None,
            0xCA: None,
            0xCB: (self.DDCB),
            0xCC: None,
            0xCD: None,
            0xCE: None,
            0xCF: None,
            0xD0: None,
            0xD1: None,
            0xD2: None,
            0xD3: None,
            0xD4: None,
            0xD5: None,
            0xD6: None,
            0xD7: None,
            0xD8: None,
            0xD9: None,
            0xDA: None,
            0xDB: None,
            0xDC: None,
            0xDD: None,
            0xDE: None,
            0xDF: None,
            0xE0: None,
            0xE1: (self.POP, ["IX"]),
            0xE2: None,
            0xE3: (self.EX, ["(SP)", "IX"]),
            0xE4: None,
            0xE5: (self.PUSH, ["IX"]),
            0xE6: None,
            0xE7: None,
            0xE8: None,
            0xE9: (self.JP, ["(IX)"]),
            0xEA: None,
            0xEB: None,
            0xEC: None,
            0xED: None,
            0xEE: None,
            0xEF: None,
            0xF0: None,
            0xF1: None,
            0xF2: None,
            0xF3: None,
            0xF4: None,
            0xF5: None,
            0xF6: None,
            0xF7: None,
            0xF8: None,
            0xF9: (self.LD, ["SP", "IX"]),
            0xFA: None,
            0xFB: None,
            0xFC: None,
            0xFD: None,
            0xFE: None,
            0xFF: None,
        }

    def consume_cycles(self, cycles):
        # Wait for the cycle quota to be high enough
        while self.cycles < cycles:
            time.sleep(0.001)
        self.cycles -= cycles

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
        self.consume_cycles(4)
        pass

    def LD(self, operand1, operand2):
        if operand1 in ["A", "B", "C", "D", "E", "H", "L"]:
            if operand2 in ["A", "B", "C", "D", "E", "H", "L"]:
                # Register to register loading
                value = self.get_register(operand2)
                self.set_register(operand1, value)
                self.consume_cycles(4)
            elif operand2 == "(HL)":
                # Memory to register loading
                address = self.get_register("HL")
                value = self.memory_mapper.read_byte(address)
                self.set_register(operand1, value)
                self.consume_cycles(7)
            else:
                raise ValueError(f"Invalid operand: {operand2}")
        elif operand1 == "(HL)":
            if operand2 in ["A", "B", "C", "D", "E", "H", "L"]:
                # Register to memory loading
                address = self.get_register("HL")
                value = self.get_register(operand2)
                self.memory_mapper.write_byte(address, value)
                self.consume_cycles(7)
            else:
                raise ValueError(f"Invalid operand: {operand2}")
        elif operand1 in ["BC", "DE", "HL", "SP"]:
            if operand2 == "d16":
                # Immediate loading
                value = self.memory_mapper.read_byte(self.get_register("PC")) | (
                    self.memory_mapper.read_byte(self.get_register("PC") + 1) << 8
                )
                self.set_register(operand1, value)
                self.consume_cycles(10)
                self.set_register("PC", self.get_register("PC") + 2)
            else:
                raise ValueError(f"Invalid operand: {operand2}")
        else:
            raise ValueError(f"Invalid operand: {operand1}")

    def DEC(self, operand):
        if operand in ["B", "C", "D", "E", "H", "L"]:
            # Decrement register
            value = self.get_register(operand)
            result = (value - 1) & 0xFF
            self.set_register(operand, result)
            self.set_flag("N", True)
            self.set_flag("H", (value & 0x0F) == 0x00)
            self.set_flag("P/V", value == 0x80)
            self.consume_cycles(4)
        elif operand == "(HL)":
            # Decrement memory
            address = self.get_register("HL")
            value = self.memory_mapper.read_byte(address)
            result = (value - 1) & 0xFF
            self.memory_mapper.write_byte(address, result)
            self.set_flag("Z", result == 0)
            self.set_flag("N", True)
            self.set_flag("H", (value & 0x0F) == 0x00)
            self.set_flag("P/V", value == 0x80)
            self.consume_cycles(11)
        elif operand in ["BC", "DE", "HL", "SP"]:
            # Decrement register
            value = self.get_register(operand)
            result = (value - 1) & 0xFFFF
            self.set_register(operand, result)
            self.consume_cycles(6)
        else:
            raise ValueError(f"Invalid operand: {operand}")
    


    def RLCA(self):
        carry = self.get_flag("C")
        self.set_flag("C", (self.A >> 7) & 1)
        self.set_register("A", ((self.A << 1) & 0xFF) | carry)
        self.set_flag("N", False)
        self.set_flag("H", False)
        self.consume_cycles(4)

    def EX(self, operand1, operand2):
        if operand1 == "(SP)":
            if operand2 in ["HL", "IX", "IY"]:
                # Exchange (HL) with register
                address = self.get_register("SP")
                value1 = self.memory_mapper.read_byte(address)
                value2 = self.memory_mapper.read_byte(address + 1)
                self.memory_mapper.write_byte(
                    address, self.get_register(operand2) & 0xFF
                )
                self.memory_mapper.write_byte(
                    address + 1, (self.get_register(operand2) >> 8) & 0xFF
                )
                self.set_register(operand2, (value2 << 8) | value1)
                self.consume_cycles(19)
            else:
                raise ValueError(f"Invalid operand: {operand2}")
        elif operand1 in ["BC", "DE", "HL", "AF"]:
            if operand2 in ["BC", "DE", "HL", "AF"]:
                # Exchange register with register
                value1 = self.get_register(operand1)
                value2 = self.get_register(operand2)
                self.set_register(operand1, value2)
                self.set_register(operand2, value1)
                self.consume_cycles(4)
            else:
                raise ValueError(f"Invalid operand: {operand2}")
        else:
            raise ValueError(f"Invalid operand: {operand1}")

    def ADD(self, operand1, operand2=None):
        if operand2 is None:
            # ADD A, r
            value = self.get_register(operand1)
            result = self.A + value
            self.set_register("A", result & 0xFF)
            self.set_flag("Z", self.A == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.A & 0x0F) + (value & 0x0F) > 0x0F)
            self.set_flag("C", result > 0xFF)
            self.set_flag("P/V", (self.A ^ value ^ result) & 0x80)
            self.consume_cycles(4)
        elif operand1 == "HL":
            # ADD HL, rr
            value = self.get_register(operand2)
            result = self.HL + value
            self.set_register("HL", result & 0xFFFF)
            self.set_flag("N", False)
            self.set_flag("H", (self.HL & 0x0FFF) + (value & 0x0FFF) > 0x0FFF)
            self.set_flag("C", result > 0xFFFF)
            self.consume_cycles(11)
        elif operand1 == "A" and operand2 == "(HL)":
            # ADD A, (HL)
            address = self.get_register("HL")
            value = self.memory_mapper.read_byte(address)
            result = self.A + value
            self.set_register("A", result & 0xFF)
            self.set_flag("Z", self.A == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.A & 0x0F) + (value & 0x0F) > 0x0F)
            self.set_flag("C", result > 0xFF)
            self.set_flag("P/V", (self.A ^ value ^ result) & 0x80)
            self.consume_cycles(7)
        elif operand1 == "A" and operand2 == "d8":
            # ADD A, d8
            address = self.get_register("PC")
            value = self.memory_mapper.read_byte(address)
            result = self.A + value
            self.set_register("A", result & 0xFF)
            self.set_flag("Z", self.A == 0)
            self.set_flag("N", False)
            self.set_flag("H", (self.A & 0x0F) + (value & 0x0F) > 0x0F)
            self.set_flag("C", result > 0xFF)
            self.set_flag("P/V", (self.A ^ value ^ result) & 0x80)
            self.set_register("PC", address + 1)
            self.consume_cycles(7)
        else:
            raise ValueError(f"Invalid operands: {operand1}, {operand2}")

    def RRCA(self):
        carry = self.get_flag("C")
        self.set_flag("C", self.A & 1)
        self.set_register("A", ((self.A >> 1) & 0xFF) | (carry << 7))
        self.set_flag("N", False)
        self.set_flag("H", False)
        self.consume_cycles(4)

    def DJNZ(self, D):
        self.set_register("B", self.get_register("B") - 1)
        if self.get_register("B") != 0:
            self.set_register("PC", self.get_register("PC") + D)
            self.consume_cycles(13)
        else:
            self.consume_cycles(8)

    def RLA(self):
        carry = self.get_flag("C")
        self.set_flag("C", self.A >> 7)
        self.set_register("A", ((self.A << 1) & 0xFF) | carry)
        self.set_flag("N", False)
        self.set_flag("H", False)
        self.consume_cycles(4)

    def RRA(self):
        carry = self.get_flag("C")
        self.set_flag("C", self.A & 1)
        self.set_register("A", ((self.A >> 1) & 0xFF) | (carry << 7))
        self.set_flag("N", False)
        self.set_flag("H", False)
        self.consume_cycles(4)

    def JR(self, D):
        self.set_register("PC", self.get_register("PC") + D)
        self.consume_cycles(12)
