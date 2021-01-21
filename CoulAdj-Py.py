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


# In[11]:


COLUMN_SEPARATOR = "\t"

"""
DO NOT CHANGE THESE HEADERS

These headers are part of the API defined in the Readme.
They MUST NOT be changed unless the major version number is incremented.

The outputted files are meant to be parsed by programs that rely on
   hardcoded column names.

THE NAMES OF THE COLUMNS, AND THE ORDER IN WHICH THEY ARE WRITTEN,
   ARE THE MOST CRITICAL PART OF THE API.

DO NOT CHANGE

DO NOT CHANGE
"""
HEADERS = {
    "RGB" : COLUMN_SEPARATOR.join(["r", "g", "b", "adj_r", "adj_g", "adj_b"]),
    "RGB_ALPHA" : COLUMN_SEPARATOR.join(["r", "g", "b", "a", "adj_r", "adj_g", "adj_b", "adj_a"])
}

def stringify():
    nbChannels = image.shape[2]
    if nbChannels == 3:
        header = HEADERS["RGB"]
    elif nbChannels == 4:
        header = HEADERS["RGB_ALPHA"]
    else:
        raise TypeError("Image must have 3 or 4 channels")
    
    sortedAdjacencies = [header]
    sortedPixels = sorted(adjacencies.keys())
    for pixel in sortedPixels:
        neighboursAsSet = adjacencies[pixel]
        sortedNeighbours = sorted(list(neighboursAsSet))
        for neighbour in sortedNeighbours:
            sortedAdjacencies.append(COLUMN_SEPARATOR.join(map(str, pixel + neighbour)))
            
    """
    TSV specification say that each line must end with EOL
    https://www.iana.org/assignments/media-types/text/tab-separated-values
    """
    joinedAdjacencies = "\n".join(sortedAdjacencies)
    conformToTsvSpecifications = joinedAdjacencies + "\n"
    return conformToTsvSpecifications

stringyfied = stringify()
print(stringyfied)


# In[ ]:




