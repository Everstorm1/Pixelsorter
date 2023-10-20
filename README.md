# Pixelsorter
This is a single code file that takes any png/jpg files as inputs, creates a mask based on an upper and lower threshold (r+g+b) and outputs:

1. A completely (horizontally) sorted image file from the output named "sortedImg.png"
2. A mask based on the set upper- and lower-Threshold variables (mask calculations are done by taking the sum of each pixels r,g,b values --> lowerTreshold = 0, upperThreshold = 766 results in the whole image being a mask a.k.a. no sorting to be done) named "MaskImg.png"
3. A masked and sorted image called "sorted_with_mask.png"


these outputs all use the specified output path. Play aound with thresholds. 

IMPORTANT:
The input path needs to contain the image files name and file type (e.g. input_path = C:/users/desktop/random_folder/input_image.png")


(and yes, ik the code is slow :(  )
