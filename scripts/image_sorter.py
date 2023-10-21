import os.path

import numpy as np
import cv2
import time
import argparse

argparser = argparse.ArgumentParser()
subp = argparser.add_subparsers(dest='command')

values = subp.add_parser('--override', help='Override Thresholds of the Program [Optional]')
values.add_argument('--lowerThreshold', type=int)
values.add_argument('--upperThreshold', type=int)

argparser.add_argument('--infile', type=str, required=True, help="Path to the Input File of this Script")
argparser.add_argument('--outfile', type=str, required=False, help="Path to the Output of this Script, defaults to the Input Name")

args = argparser.parse_args()

start_time = time.time()

input_path = args.infile

if args.outfile is not None:
    output_path = args.outfile

else:
    output_path = os.path.dirname(input_path)

if not output_path.endswith('\\'):
    output_path += '\\'

if args.command == 'override':
    if args.lowerThreshold is not None:
        lowerThreshold = args.lowerThreshold
    else:
        lowerThreshold = 320


    if args.upperThreshold is not None:
        upperTheshold = args.upperThreshold

    else:
        upperTheshold = 500

else:
    lowerThreshold = 320
    upperTheshold = 500

inp_img = cv2.imread(input_path)
width = inp_img.shape[1]
height = inp_img.shape[0]



new_image = np.zeros((height, width, 3), dtype=np.uint8)

for i in range(3):
    for a in range(height):
        new_image[a, :, i] = inp_img[a, :, i]


sums = new_image.sum(axis=2)

sorted_indices = sums.argsort(axis=1)
sorted_image = np.empty_like(new_image)

for i in range(height):
    sorted_image[i, :, :] = new_image[i, sorted_indices[i], :]

elapsed_time = time.time() - start_time
print(f"time for creating sorted IMG: {elapsed_time:.2f} seconds")

# save sorted IMG
cv2.imwrite(output_path + "sortedImg.png", sorted_image)

#-----------------------------------------------------------

new_mask = np.empty_like(new_image)
for i in range(height):
    for a in range(width):
        if lowerThreshold < sums[i][a] < upperTheshold:
            new_mask[i][a][:] = (255, 255, 255)
        else:
            new_mask[i][a][:] = (0, 0, 0)

elapsed_time = time.time() - start_time
print(f"time for creating mask: {elapsed_time:.2f} seconds")

# save mask
cv2.imwrite(output_path + "MaskImg.png", new_mask)

#------------------------------------------------------------

mask_sum = new_mask.sum(axis=2)
masked_img = np.empty_like(new_image)
spaces_List = []

for i in range(height):
    counter = 0
    spaces = []
    for value in mask_sum[i]:

        #security for beginning of images
        if mask_sum[i][0] == 0 and counter == 0:
            spaces.append(counter)

        if mask_sum.shape[1] > counter + 1:
            if value == 0 and mask_sum[i][counter + 1] >= 1:
                spaces.append(counter)
        
        if value == 0 and mask_sum[i][counter - 1] >= 1:
                spaces.append(counter)
        
        counter += 1

    #security for end of images
    if mask_sum[i][mask_sum.shape[1] - 1] == 0:
        spaces.append(mask_sum.shape[1] - 1)


    spaces_List.append(spaces)
    

spaces_array = np.array(spaces_List, dtype=object)

elapsed_time = time.time() - start_time
print(f"time for creating space measures: {elapsed_time:.2f} seconds")

#---------------------------------------------------------------------------

snippet_list = []
for i in range(height):
    sorted_snippet = []

    for x in range(int(len(spaces_array[i]) / 2)):
        #print(str(x * 2) + " / " + str((x * 2)+1))

        if spaces_array[i][x * 2] == spaces_array[i][(2 * x) + 1]:
            add = new_image[i, spaces_array[i][x * 2], :].reshape(1, -1)
        else:
            add = new_image[i, spaces_array[i][x * 2]:spaces_array[i][(2 * x) + 1] + 1, :]

        sorted_indices = add.sum(axis=1).argsort()
        sorted_snippet.append(add[sorted_indices, :])

    snippet_list.append(sorted_snippet)
    
snippet_array = np.array(snippet_list, dtype=object)

elapsed_time = time.time() - start_time
print(f"time for creating array of sorted snippets: {elapsed_time:.2f} seconds")

#-----------------------------------------------------------------

result_img = inp_img.copy()

for i in range(spaces_array.shape[0]):
    for j in range(len(spaces_array[i]) // 2):
        start_x = spaces_array[i][j * 2]
        end_x = spaces_array[i][j * 2 + 1]

        if start_x != end_x:
            # Get the sorted snippet
            snippet = snippet_array[i][j]

            # Place the sorted snippet back into the result_img
            result_img[i, start_x:end_x + 1, :] = snippet

elapsed_time = time.time() - start_time
print(f"time for stitching da shiat back togethaa: {elapsed_time:.2f} seconds")

#------------------------------------------------------------------------

# Save the result image
cv2.imwrite(output_path + "sorted_with_mask.png", result_img)
