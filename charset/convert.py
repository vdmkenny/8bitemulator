from PIL import Image
import PIL.ImageOps

INPUT_FILE="charset.bmp"
OUTPUT_FILE="charset.bin"

# Open the charset image
im = Image.open(INPUT_FILE)

# Check if image is 1-bit pallet
if(int(im.mode)!=1):
    print('This is not a 1-bit black and white file!')
    print(f'Image mode for this file is: {im.mode}')
    im.close()
    exit(1)

# Reverse image so black = 1
im = PIL.ImageOps.invert(im)

# Get properties
width, height = im.size

# Open the output file
newFile = open("charset.bin", "wb")

# Loop through the image, cropping 1 8x8 character at a time
for y in range(int(height/8)):
    for x in range(int(width/8)):
        crop_tuple =((x*8), 
                     (y*8), 
                     (width-(width-(x*8)-8)), 
                     (height-(height-(y*8)-8)))
        character = im.crop(crop_tuple)
        newFile.write(bytearray(character.tobytes()))

print(f'Binary file written to {OUTPUT_FILE}')

im.close()
