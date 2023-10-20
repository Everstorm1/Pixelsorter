import numpy as np
import cv2
import time

start_time = time.time()

output_path = "C:/Users/Ayen Wohlberg/Desktop/pixelsorter/testimg_generation/"
#input_path = "C:/Users/Ayen Wohlberg/Desktop/pixelsorter/testimg_generation/custom_colors.png"
input_path = "C:/Users/Ayen Wohlberg/Desktop/pixelsorter/testimg_generation/TestImg.png"

inp_img = cv2.imread(input_path)
width = inp_img.shape[1]
height = inp_img.shape[0]

lowerThreshold = 320
upperTheshold = 500

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


'''
print("-------------")
print("-------------")
print(new_image)
print("-------------")
#print(sorted_image)
#print("-------------")
#print(sums)
print("-------------")
#print(sorted_indices)

#print(sums.shape[1])

#print(new_mask)

print(mask_sum)
'''

# Save the result image
cv2.imwrite(output_path + "sorted_with_mask.png", result_img)