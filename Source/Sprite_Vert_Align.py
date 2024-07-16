from PIL import Image

# List of image paths
frames = 12 + 63
image_paths = []

## Cross-Sprite framing
for j in range(1, frames - 63 + 1) :
    image_paths.append("Assets\\Characters\\Pi\\Digitalized_PI\\Main\\mainPI_" + str(j) + ".png")

for i in range(0, frames - 12) :
    if i < 10 :
        image_paths.append("Assets\\Characters\\Pi\\Digitalized_PI\\Digit_PI_Rotation\\SpriteSheet\\PI_0" + str(i) + ".png")
    else :
        image_paths.append("Assets\\Characters\\Pi\\Digitalized_PI\\Digit_PI_Rotation\\SpriteSheet\\PI_" + str(i) + ".png")
        

# Open all images and get their sizes
images = [Image.open(path) for path in image_paths]
widths, heights = zip(*(i.size for i in images))

# Calculate total width and height for the new image
total_width = max(widths)
total_height = sum(heights)

# Create a new image with the calculated size
new_image = Image.new("RGBA", (total_width, total_height))

# Paste each image into the new image, horizontaly aligned
x_offset = 0
for image in images:
    new_image.paste(image, (0, x_offset))
    x_offset += image.size[1]

# Save the new image
new_image.save("Digit_Pi_Rotation(538 x 464).png")