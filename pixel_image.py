from PIL import Image

img = Image.open('images//test_image.png')
pixels = img.load() 
width, height = img.size

for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]

        print(x, y, r, g, b)