# Pixelsorter
This is a single code file that takes any png/jpg files as inputs, creates a mask based on an upper and lower threshold (r+g+b) and outputs:

1. A completely (horizontally) sorted image file from the output named "sortedImg.png"
2. A mask based on the set upper- and lower-Threshold variables (mask calculations are done by taking the sum of each pixels r,g,b values --> lowerTreshold = 0, upperThreshold = 766 results in the whole image being a mask a.k.a. no sorting to be done) named "MaskImg.png"
3. A masked and sorted image called "sorted_with_mask.png"


these outputs all use the specified output path. Play aound with thresholds. 

IMPORTANT:
The input path needs to contain the image files name and file type (e.g. input_path = C:/users/desktop/random_folder/input_image.png")


(and yes, ik the code is slow :(  )


# Usage

Shown below are a simple Example Usage to this little Script and a Command to learn more about the available Arguments
### Example Usage:
```console
python3 image_sorter.py --infile example.jpeg
```

This will create all Images from the Input-File `example.jpeg` and outputs the processed Immages with the Appropiate Suffixes.

### Getting Help:

```console
python3 image_sorter.py -h
```

This neat little Command will output all available Arguments and Positionals.


# Installation

Installation of Dependencies is really simple with this Project as we went forward to create a neat `requirements.txt` file for you.

1. Clone this Repository to your Machine, make sure to have Python installed.
	If not you can get it [here](https://www.python.org/downloads/)
2. Install the Required Dependencies
	You can Install all required Dependencies with
```console
pip -r requirements.txt
```
3. Have Fun with the Script