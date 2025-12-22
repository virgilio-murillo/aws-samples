from PIL import Image, ImageDraw
import os

# Create a simple test image
width, height = 200, 200
image = Image.new('RGB', (width, height), color='lightblue')
draw = ImageDraw.Draw(image)

# Draw a simple pattern
draw.rectangle([50, 50, 150, 150], fill='red', outline='black', width=3)
draw.ellipse([75, 75, 125, 125], fill='yellow')

# Save the test image
image.save('test_input.jpg', 'JPEG')
print("Created test_input.jpg")
