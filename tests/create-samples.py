import numpy as np

blue_12     = ( 10,  20, 230, 252)
green_10    = ( 10, 220,  30, 250)
cyan_8      = ( 10, 220, 230, 248)
red_6       = (210,  20,  30, 246)
magenta_4   = (210,  20, 230, 244)
yellow_2    = (210, 220,  30, 242)

blu = blue_12   
gre = green_10  
cya = cyan_8    
red = red_6     
mag = magenta_4 
yel = yellow_2  

cells = [
    [ yel, yel, yel, yel, yel, mag, mag, mag, red ],
    [ yel, yel, yel, yel, cya, mag, mag, mag, mag ],
    [ gre, gre, yel, yel, cya, cya, cya, cya, mag ],
    [ gre, gre, yel, yel, cya, cya, cya, cya, mag ],
    [ gre, gre, gre, gre, blu, blu, blu, blu, mag ],
    [ gre, gre, gre, gre, blu, blu, blu, blu, mag ],
    [ gre, gre, gre, gre, blu, blu, blu, blu, mag ],
    [ gre, gre, red, red, red, red, blu, blu, mag ]
]

def print_pixel_data(pythonList):
    titles = ["row", "col","r", "g", "b", "a"]
    header = "\t".join(titles)
    print(header)
    for rowIx, row in enumerate(pythonList):
        for colIx, pixel in enumerate(row):
            print(rowIx, colIx, *pixel, sep="\t")

size = 2
factor = 2**size

# Init matrix of None
nbRows = factor * len(cells)
nbCols = factor * len(cells[0])
maxRow = nbRows - 1
maxCol = nbCols - 1
pythonList = [
    [None for c in range(nbCols)] for r in range(nbRows)
]

def fill_cell(pythonList, cellRow, cellCol, cellValue, factor):
    originRow = cellRow * factor
    originCol = cellCol * factor
    lastRow = originRow + factor
    lastCol = originCol + factor
    for pixelRow in range(originRow, lastRow):
        for pixelCol in range(originCol, lastCol):
            pythonList[pixelRow][pixelCol] = cellValue

for cellRow, row in enumerate(cells):
    for cellCol, cell in enumerate(row):
            fill_cell(pythonList, cellRow, cellCol, cell, factor)

# I want the top right colour to always be a single pixel.
fill_cell(pythonList, 0, -1, cells[0][-2], factor)
pythonList[0][-1] = cells[0][-1]

print_pixel_data(pythonList)

