import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

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

size = 1024
savefilename = "sample-size-1024.png"
nbCellRows = len(cells)
nbCellCols = len(cells[0])
nbRows = size * nbCellRows 
nbCols = size * nbCellCols 
print(nbCellRows, nbCellCols, nbRows, nbCols)

maxCellRow = nbCellRows - 1
maxCellCol = nbCellCols - 1
maxRow = nbRows - 1
maxCol = nbCols - 1
print(maxCellRow, maxCellCol, maxRow, maxCol)

width = nbCols
height = nbRows
print(width, height)
im = Image.new("RGBA", (width, height), (0,0,0,255))
d = ImageDraw.Draw(im)

#plt.imshow(im)
#plt.show()


def rowCol_to_XY(row, col):
    return {"X": col, "Y": row}

def rowCol_to_XY_tuple(row, col):
    xy = rowCol_to_XY(row, col)
    return(xy["X"], xy["Y"])


def fill_rectangle(cellRow, cellCol, colour=None):
    cellXY = rowCol_to_XY(cellRow, cellCol)
    rectX0 = size * cellXY["X"]
    rectY0 = size * cellXY["Y"]
    rectX1 = rectX0 + size
    rectY1 = rectY0 + size
    rectXY = [rectX0, rectY0, rectX1, rectY1]
    colour = cells[cellRow][cellCol] if colour is None else colour
    d.rectangle(rectXY, fill=colour, outline=colour, width=0)
    

for cellRow in range(nbCellRows):
    for cellCol in range(nbCellCols):
        fill_rectangle(cellRow, cellCol)

# Corner coordinates
topLeftPixel = rowCol_to_XY_tuple(     0,      0)
topRighPixel = rowCol_to_XY_tuple(     0, maxCol)
botLeftPixel = rowCol_to_XY_tuple(maxRow,      0)
botRighPixel = rowCol_to_XY_tuple(maxRow, maxCol)
        
# Make top-right cell always 1x1 pixels
lonePixelColour = cells[0][-1]
surroundingColour = cells[0][-2]
fill_rectangle(0, maxCellCol, surroundingColour)
im.putpixel(topRighPixel, lonePixelColour)


plt.axis("off")
plt.imshow(im)
plt.show()

print(im.getpixel(topLeftPixel), im.getpixel(topRighPixel))
print(im.getpixel(botLeftPixel), im.getpixel(botRighPixel))

im.save(savefilename)