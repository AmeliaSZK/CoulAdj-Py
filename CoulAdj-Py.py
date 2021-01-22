import imageio
import numpy as np
import time


# # Dev stuff
# 
# Specify where _in this repo_ the input and output files are.


samples = {
    "small" : "tests/small.bmp",
    "small-alpha" : "tests/small-alpha.bmp",
    "shadow" : "tests/proprietary/warhammer_map_1_1_shadow.bmp",
    "vortex" : "tests/proprietary/wh2_main_great_vortex_map_6.bmp"
}
results = {
    "small" : "tests/result small.tsv",
    "small-alpha" : "tests/result small-alpha.tsv",
    "shadow" : "tests/proprietary/result warhammer_map_1_1_shadow.tsv",
    "vortex" : "tests/proprietary/result wh2_main_great_vortex_map_6.tsv"
}


# # Selection of Sample to Test
# 
# Choose the test to run here.
# 
# If you don't have the proprietary images, pick either `"small"` or `"small-alpha"`.
# (You almost certainly don't have them)

test = "shadow"


# # Input
# 
# (Don't) Write your inputs here:
# 
# (During development, specify your input in the section above.)


source = samples[test]
destination = results[test]
relateDiagonals = True # Default is True
print(source)
print(destination)


# # Processing

image = imageio.imread(source)
print(image.shape)
print(image.meta)

adjacencies = dict()
nbRows = image.shape[0]
nbColumns = image.shape[1]
maxRow = nbRows - 1
maxColumn = nbColumns -1
print(nbRows, nbColumns, maxRow, maxColumn)

startTime = time.perf_counter()

TOP_OFFSET = -1
BOT_OFFSET = 1
LEF_OFFSET = -1
RIG_OFFSET = 1

def process_top_left_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)

def process_top_right_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, LEF_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)

def process_bottom_left_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

def process_bottom_right_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, LEF_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

def process_top_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)

def process_bottom_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

def process_left_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

def process_right_pixel(pixelRow, pixelColumn):
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, LEF_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

def process_middle_pixel(pixelRow, pixelColumn):
    if pixelColumn == 1 and pixelRow % 10 == 0:
        print("Now starting pixel at row {} and column {}".format(pixelRow, pixelColumn))
        if pixelRow == 50:
            endTime = time.perf_counter()
            duration = round(endTime - startTime, 2)
            print(duration)
            quit()
    pixelColour = image[pixelRow, pixelColumn].tobytes()
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)
    #if relateDiagonals:
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

        
def process_neighbour(pixelColour, pixelRow, pixelColumn, rowOffset, columnOffset):
    neighRow = pixelRow + rowOffset
    neighColumn = pixelColumn + columnOffset
    neighColour = image[neighRow, neighColumn].tobytes()
    if pixelColour == neighColour: 
        return
    adjacencies.setdefault(pixelColour, set()).add(neighColour)
    
    
def valid_row_column(row, column):
    return (0 <= row <= maxRow
           and 0 <= column <= maxColumn)

def same_colours(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True

# Corners
process_top_left_pixel(0, 0)
process_top_right_pixel(0, maxColumn)
process_bottom_left_pixel(maxRow, 0)
process_bottom_right_pixel(maxRow, maxColumn)

# Edges
for column in range(1, nbColumns-1):
    process_top_pixel(0, column)
    process_bottom_pixel(maxRow, column)

for row in range(1, nbRows-1):
    process_left_pixel(row, 0)
    process_right_pixel(row, maxColumn)

# Middle
for row in range(1, nbRows-1):
    for column in range(1, nbColumns-1):
        process_middle_pixel(row, column)


# # Output


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


with open(destination, "w") as file:
    file.write(stringyfied)

