from PIL import Image

# List of image paths
frames = 95
image_paths = []

for i in range(1,frames) :
    if i < 10 :
        image_paths.append("Assets\\Scoreboard\\Intro Animation\\sB0" + str(i) + ".png")
    else :
        image_paths.append("Assets\\Scoreboard\\Intro Animation\\sB" + str(i) + ".png")
        

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
new_image.save("Scoreboard Intro(1332 x 697).png")