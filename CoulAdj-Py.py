#!/usr/bin/env python
# coding: utf-8

# In[1]:


import imageio
import numpy as np


# # Dev stuff

# In[2]:


samples = {
    "small" : "tests/small.bmp",
    "small-alpha" : "tests/small-alpha.bmp",
    "shadow" : "tests/proprietary/warhammer_map_1_1_shadow.bmp",
    "vortex" : "tests/proprietary/wh2_main_great_vortex_map_6.bmp"
}


# # Input
# Write your inputs here:

# In[3]:


source = samples["small-alpha"]
relateDiagonals = True # Default is True
print(source)


# # Process
# (Output is after this section)

# In[4]:


image = imageio.imread(source)
print(image.shape)
print(image.meta)

adjacencies = dict()
nbRows = image.shape[0]
nbColumns = image.shape[1]
maxRow = nbRows - 1
maxColumn = nbColumns -1
print(nbRows, nbColumns, maxRow, maxColumn)


# In[5]:


# Print pixel data for debug
print("\t".join(["row", "col", "r", "g", "b", "a"]))
for row in range(nbRows):
    for column in range(nbColumns):
        print(row, column, "\t".join(map(str, image[row, column])), sep="\t")
        
R_INDEX = 0
G_INDEX = 1
B_INDEX = 2
A_INDEX = 3


# In[6]:


def process_pixel(pixelRow, pixelColumn):
    pixelColour = tuple(image[pixelRow, pixelColumn].tolist())
    process_neighbour(pixelColour, pixelRow, pixelColumn, 1, -1)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 1, 1)
    process_neighbour(pixelColour, pixelRow, pixelColumn, -1, -1)
    process_neighbour(pixelColour, pixelRow, pixelColumn, -1, 1)
    if relateDiagonals:
        process_neighbour(pixelColour, pixelRow, pixelColumn, 1, 0)
        process_neighbour(pixelColour, pixelRow, pixelColumn, 0, 1)
        process_neighbour(pixelColour, pixelRow, pixelColumn, 0, -1)
        process_neighbour(pixelColour, pixelRow, pixelColumn, -1, 0)

        
def process_neighbour(pixelColour, pixelRow, pixelColumn, rowOffset, columnOffset):
    neighRow = pixelRow + rowOffset
    neighColumn = pixelColumn
    if not valid_row_column(neighRow, neighColumn): 
        return
    neighColour = tuple(image[neighRow, neighColumn].tolist())
    if same_colours(pixelColour, neighColour): 
        return
    adjacencies.setdefault(pixelColour, set()).add(neighColour)
    
    
def valid_row_column(row, column):
    return (0 <= row
           and 0 <= column
           and row <= maxRow
           and column <= maxColumn)

def same_colours(a, b):
    if len(a) != len(b):
        raise TypeError("Colours from the same image should have the same number of channels.")
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


for row in range(nbRows):
    for column in range(nbColumns):
        process_pixel(row, column)

print(adjacencies)


# In[ ]:




