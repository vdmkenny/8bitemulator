import pygame

import struct

from z80 import Z80


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the window
    screen = pygame.display.set_mode((160, 144))
    pygame.display.set_caption("Z80 Emulator")

    # Create a clock for controlling the frame rate
    clock = pygame.time.Clock()

    computer = Z80()
    video_memory_address = 0xC000
    character_rom_address = 0xE000

    # Main game loop
    running = True
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        # Draw the pixels to the screen
        for y in range(18):
            for x in range(20):
                print(
                    f"trying to fetch memory address {hex(video_memory_address + x * y)}"
                )

                low_byte = computer.memory_mapper.read_byte(
                    video_memory_address + (x * y * 2)
                )
                high_byte = computer.memory_mapper.read_byte(
                    video_memory_address + (x * y * 2) + 1
                )

                result = low_byte + (high_byte << 8)
                char_offset = int.from_bytes(
                    result.to_bytes(2, byteorder="little"), byteorder="little"
                )

                for char_y in range(8):
                    for char_x in range(8):
                        row_value = computer.memory_mapper.read_byte(
                            character_rom_address + char_offset + (char_x * char_y)
                        )
                        binary_string = bin(row_value)[2:].zfill(8)
                        pixel_value = binary_string[char_x]
                        if pixel_value == 0:
                            color = (0, 0, 0)
                        else:
                            color = (255, 255, 255)
                        screen.set_at((char_x + (x * 8), char_y + (y * 8)), color)

        # Update the display
        pygame.display.flip()

        # Wait to maintain 60fps
        clock.tick(60)

    # Clean up and exit
    pygame.quit()


if __name__ == "__main__":
    main()
