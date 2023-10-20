import numpy as np
import cv2
import os
import random

custom_colors = [
    (255, 20, 0),  # Red
    (0, 255, 100),  # Green
    (10, 0, 25),  # Blue
    (180, 255, 20),  # Yellow
    (90, 80, 150),  # Magenta
    (0, 255, 10),
    (200, 10, 10),
    (100, 50, 1),
    (255, 100, 2),
    (100, 100, 0),
    (0, 0, 0)
]

output_path = "C:/Users/"
input_path = "C:/Users/"

# Define the dimensions of the image
width, height = 11, 2

# Create an image with custom colors
image = np.zeros((height, width, 3), dtype=np.uint8)

for a in range(height):
    # Fill the image with custom colors
    for i, color in enumerate(custom_colors):
        start_x = i * (width // len(custom_colors))
        end_x = (i + 1) * (width // len(custom_colors))
        image[a, start_x:end_x, :] = color

print(image)

# Save the image
cv2.imwrite(output_path + "custom_colors.png", image)

inp_img = cv2.imread(input_path)

if inp_img[0][0][0] == image[0][0][0]:
    print("hi")
    
