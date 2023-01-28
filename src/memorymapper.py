from romloader import ROMLoader

import random


class MemoryMapper:
    def __init__(self):
        self.program_rom = bytearray(0x8000)  # 32K (0x0000 - 0x7FFF)
        self.ram = bytearray(0x4000)  # 16K (0x8000 - 0xBFFF)
        self.video_memory = bytearray(0x2000)  # 8K  (0xC000 - 0xDFFF)
        self.character_rom = bytearray(0x1000)  # 4K  (0xE000 - 0xEFFF)
        self.reserved_space = bytearray(0x1000)  # 4K  (0xF000 - 0xFFFF)
        self.read_only_sections = {
            "program_rom": range(0x0000, 0x7FFF),
            "character_rom": range(0xE000, 0xEFFF),
        }

        # Init the ROMs
        program_rom_loader = ROMLoader("../program.bin", 0x8000)
        self.program_rom = program_rom_loader.load()

        character_rom_loader = ROMLoader("../charset.bin", 0x1000)
        self.character_rom = character_rom_loader.load()

        # put some garbage in video ram for now, DELETE THIS LATER IN DEVELOPMENT
        for i in range(0, len(self.video_memory), 2):
            #            self.video_memory[i] = random.randint(0,20) * 8
            #            self.video_memory[i+1] = random.randint(0,3)

            self.video_memory[i] = 0x00
            self.video_memory[i + 1] = 0x00

        self.video_memory[0] = 0x40  # H
        self.video_memory[1] = 0x01
        self.video_memory[2] = 0x28  # E
        self.video_memory[3] = 0x01
        self.video_memory[4] = 0x60  # L
        self.video_memory[5] = 0x01
        self.video_memory[6] = 0x60  # L
        self.video_memory[7] = 0x01
        self.video_memory[8] = 0x78  # O
        self.video_memory[9] = 0x01
        self.video_memory[10] = 0x00  # space
        self.video_memory[11] = 0x00
        self.video_memory[12] = 0xB8  # W
        self.video_memory[13] = 0x01
        self.video_memory[14] = 0x78  # O
        self.video_memory[15] = 0x01
        self.video_memory[16] = 0x90  # R
        self.video_memory[17] = 0x01
        self.video_memory[18] = 0x60  # L
        self.video_memory[19] = 0x01
        self.video_memory[20] = 0x20  # D
        self.video_memory[21] = 0x01
        self.video_memory[22] = 0x08  # !
        self.video_memory[23] = 0x00

    def read_byte(self, address):
        if address < 0x8000:
            return self.program_rom[address]
        elif address < 0xC000:
            return self.ram[address - 0x8000]
        elif address < 0xE000:
            return self.video_memory[address - 0xC000]
        elif address < 0xF000:
            return self.character_rom[address - 0xE000]
        else:
            return self.reserved_space[address - 0xF000]

    def write_byte(self, address, value):
        if address in self.read_only_sections.values():
            print("ERROR: Attempted to write to ROM!")
            return
        elif address < 0x8000:
            self.program_rom[address] = value
        elif address < 0xC000:
            self.ram[address - 0x8000] = value
        elif address < 0xE000:
            self.video_memory[address - 0xC000] = value
        elif address < 0xF000:
            self.character_rom[address - 0xE000] = value
        else:
            self.ram[address - 0xF000] = value
