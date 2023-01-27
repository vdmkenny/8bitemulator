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
        for i in range(len(self.video_memory)):
            self.video_memory[i] = random.randint(0x0001, 0x0016)

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
