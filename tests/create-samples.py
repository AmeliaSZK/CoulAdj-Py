import numpy as np
from PIL import Image, ImageDraw

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

size = 1
nbX = size * len(cells) # rows
nbY = size * len(cells[0]) # columns
width = nbY
height = nbX
maxX = nbX - 1
maxY = nbY - 1

im = Image.new("RGBA", (width, height))
d = ImageDraw.Draw(im)


