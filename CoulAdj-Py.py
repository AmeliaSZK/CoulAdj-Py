# coding=utf-8
# Computes, for each colour in the image, the list of all adjacent colours.
# Copyright (C) 2021  Amélia SZK <amelia.szk@protonmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import imageio
import numpy as np
import argparse
import time
import logging
import sys

version = "0.1"

# ##### PROLOGUE #####
# ~~~ Profiling ~~~
startTime = time.perf_counter()

# ~~~ Command Line Interface ~~~
diags_flags = ("-d", "--dont-relate-diagonals")
verbose_flags = ("-v", "--verbose")
version_flags = ("-n", "--version")

profile_flags = ("-p", "--profile")
debug_flags = ("-g", "--debug")

description_program = "Computes, for each colour in the image," \
    " the list of all adjacent colours and writes the results to a TSV file."
epilog_program = "CoulAdj-Py  Copyright (C) 2021  Amélia SZK."

help_diags = "if present, will only consider the 4 neighbours with a common edge" \
    " (top, bottom, left, right) to be adjacent." \
    " By default, all 8 neighbours are considered adjacent"
help_verbose = "display informations about the file and the computations"
help_img = "The image file to process."
help_res = "The TSV file in which to write the results. " \
    "If it already exists, it will be erased and overwritten."

parser = argparse.ArgumentParser(
    description=description_program, 
    epilog=epilog_program,
    exit_on_error=True) # To delegate file IOs as much as possible.

parser.add_argument(*diags_flags, help=help_diags,
    action="store_true", dest="dontRelateDiagonals")
parser.add_argument(*verbose_flags, help=help_verbose,
    action="store_true")
parser.add_argument(*version_flags, 
    action="version", version="%(prog)s " + version)

parser.add_argument("image", help=help_img, 
    type=argparse.FileType("rb"))
parser.add_argument("results", help=help_res, 
    type=argparse.FileType("w"))

parser.add_argument(*profile_flags, help=argparse.SUPPRESS,
    action="store_true") # Prints the execution time to stderr regardless of logging level
parser.add_argument(*debug_flags, help=argparse.SUPPRESS,
    action="store_true") # Sets logging level to DEBUG. Overrides --verbose

args = parser.parse_args()

# ~~~ Logging ~~~
if args.debug:
    loglevel = logging.DEBUG
elif args.verbose:
    loglevel = logging.INFO
else:
    loglevel = logging.WARNING

logging.basicConfig(encoding='utf-8', format='%(levelname)s:%(message)s', level=loglevel)

# ##### CONSTANTS #####
TOP_OFFSET = -1
BOT_OFFSET = 1
LEF_OFFSET = -1
RIG_OFFSET = 1

# ##### CONVERSION FUNCTIONS #####
# These followings are all different ways of representing the
#   *same* pixel colour:
#
# `pixelData` 
#       A library converts the image file into a 2D array of pixelData
# `colourKey`
#       We convert the pixelData to a `colourKey` to store the colour
#       in sets and dictionaries. 
# `RGBA`
#       We convert `colourKey` to a tuple of (red, green, blue, alpha) for
#       two purposes that must be done in this order:
#           1) Sort the colours
#           2) Craft the output strings
#       And yes, it MUST be a *tuple* of (red, green, blue, alpha).
#
# Additionally, we have:
#
# `relation`
#       A record of two RGBA colours adjacent to each others.
#       More specifically, it is a one-way directed relation. So to represent
#       one "adjacency", we need two "relations".
#
# ~~~ Program Outline ~~~
# Optimizing the program to an acceptable level of performance involves a lot
#   experimentation with data types and conversions.
# In order to make this experimentation more convenient, we establish a
#   hard decoupling betwen the processing and the output crafting.
#
# More specifically, a general outline of the program is:
#   1) Import
#       From the image filepath, construct a 2D array of colours
#
#   2) Calculate Adjacencies
#       From that 2D array, construct a dictionary of colours (keys) and
#       sets of adjacent colours (values)
#
#   3) Sort
#       From that dictionary, construct a list of `relations`, and sort it
#
#   4) Stringify
#       From that sorted list, craft the list of lines to write in the TSV file
#
#   5) Write
#       Take that list of lines, and write them to the TSV file
#
# The hard boundary we are establishing is between #2 and #3:
#   1) Import
#   2) Calculate Adjacencies
#   ~~~ BOUNDARY HERE ~~~
#   3) Sort
#   4) Stringify
#   5) Write
#
# More specifically, this means that the Sort section expects to work with
#   a dictionary of `colourKey` as keys, and a set of `colourKey` as values.
# So Import & Calculate Adjacencies can introduce coupling to optimize, and
#   Sort, Stringify, & Write can also take shortcuts between each others,
# But at the boundary, it MUST be the expected dict that is passed.
#
# Furthermore, while RGBA_from_colourKey may have been previously defined,
#   the sections before the Boundary are responsible for making sure that the 
#   correct conversion function has been assigned to RGBA_from_colourKey.
#       (Yes, I know that have more than 1 responsible is asking for trouble,
#       but as I am writing these lines, the new outline has not been 
#       implemented yet so things will probably evolve.)

def uintc_from_pixelData(pixelData: np.ndarray):
    r = pixelData[0] << 24
    g = pixelData[1] << 16
    b = pixelData[2] << 8
    a = pixelData[3] << 0
    return r + g + b + a

def RGBA_from_uintc(x):
    r = x >> 24 & 0x000000FF
    g = x >> 16 & 0x000000FF
    b = x >> 8 & 0x000000FF
    a = x >> 0 & 0x000000FF
    return (r, g, b, a)

def colourKey_from_pixelData(pixelData: np.ndarray):
    return uintc_from_pixelData(pixelData)

# ~~~ BOUNDARY ~~~
def RGBA_from_colourKey(colourKey):
    return RGBA_from_uintc(colourKey)
# ~~~ BOUNDARY ~~~

def relation_from_two_RGBAs(rgba1, rgba2):
    return (rgba1, rgba2)

def colour_RGBA_from_relation(relation):
    return relation[0]

def adjacent_RGBA_from_relation(relation):
    return relation[1]

def red_from_RGBA(rgba):
    return rgba[0]

def green_from_RGBA(rgba):
    return rgba[1]

def blue_from_RGBA(rgba):
    return rgba[2]

def alpha_from_RGBA(rgba):
    return rgba[3]



# ##### INPUTS #####
source = args.image
destination = args.results
relateDiagonals = not args.dontRelateDiagonals
logging.info("Starting")

# ##### IMPORT #####
image = imageio.imread(source)
height = image.shape[0]
width = image.shape[1]
nbChannels = image.shape[2]
logging.info("Height = {}, Width = {}, {} channels".format(height, width, nbChannels))

adjacencies = dict()
nbRows = height
nbColumns = width
maxRow = nbRows - 1
maxColumn = nbColumns -1
logging.debug("nbRows={}, nbColumns={}, maxRow={}, maxColumn={}"
    .format(nbRows, nbColumns, maxRow, maxColumn))
topRow = 0
botRow = maxRow
lefCol = 0
rigCol = maxColumn
logging.debug("topRow={}, botRow={}, lefCol={}, rigCol={}"
    .format(topRow, botRow, lefCol, rigCol))

image_asColour = np.apply_along_axis(uintc_from_pixelData, 2, image)

# ##### CALCULATE ADJACENCIES #####

def process_pixel_with_diagonals(pixelRow, pixelColumn):
    pixelColour = image_asColour[pixelRow, pixelColumn]
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)


def process_pixel_with_valid_neighbours_with_diagonals(pixelRow, pixelColumn):
    pixelColour = image_asColour[pixelRow, pixelColumn]
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)


def process_pixel_sans_diagonals(pixelRow, pixelColumn):
    pixelColour = image_asColour[pixelRow, pixelColumn]
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)


def process_pixel_with_valid_neighbours_sans_diagonals(pixelRow, pixelColumn):
    pixelColour = image_asColour[pixelRow, pixelColumn]
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
    process_valid_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)


if relateDiagonals:
    process_pixel = process_pixel_with_diagonals
else:
    process_pixel = process_pixel_sans_diagonals

if relateDiagonals:
    process_pixel_with_valid_neighbours = process_pixel_with_valid_neighbours_with_diagonals
else:
    process_pixel_with_valid_neighbours = process_pixel_with_valid_neighbours_sans_diagonals
# Yes, I tried writing these function assignations with both the ternary 
#   operator and only one if-else. And both were hecking eyesores imo.
#   (The problem is probably with the length of the function names...)


def process_neighbour(pixelColour, pixelRow, pixelColumn, rowOffset, columnOffset):
    neighRow = pixelRow + rowOffset
    neighColumn = pixelColumn + columnOffset
    if not valid_row_column(neighRow, neighColumn): 
        return
    neighColour = image_asColour[neighRow, neighColumn]
    if pixelColour == neighColour: 
        return
    adjacencies.setdefault(pixelColour, set()).add(neighColour)
    adjacencies.setdefault(neighColour, set()).add(pixelColour)
        

def process_valid_neighbour(pixelColour, pixelRow, pixelColumn, rowOffset, columnOffset):
    neighRow = pixelRow + rowOffset
    neighColumn = pixelColumn + columnOffset
    #if not valid_row_column(neighRow, neighColumn): 
    #    return
    neighColour = image_asColour[neighRow, neighColumn]
    if pixelColour == neighColour: 
        return
    adjacencies.setdefault(pixelColour, set()).add(neighColour)
    adjacencies.setdefault(neighColour, set()).add(pixelColour)
    
    
def valid_row_column(row, column):
    return (0 <= row
           and 0 <= column
           and row <= maxRow
           and column <= maxColumn)

#def same_colours(a, b):
#    if len(a) != len(b):
#        raise TypeError("Colours from the same image should have the same number of channels.")
#    for i in range(len(a)):
#        if a[i] != b[i]:
#            return False
#    return True

# ~~~ Corners ~~~
# ~ Top Left ~
process_pixel(topRow, lefCol)
# ~ Top Right ~
process_pixel(topRow, rigCol)
# ~ Bottom Left ~
process_pixel(botRow, lefCol)
# ~ Bottom Right ~
process_pixel(botRow, rigCol)

# ~~~ Edges ~~~
# ~ Top ~
for column in range(1, nbColumns - 1):
    process_pixel(topRow, column)
# ~ Bottom ~
for column in range(1, nbColumns - 1):
    process_pixel(botRow, column)
# ~ Left ~
for row in range(1, nbRows - 1):
    process_pixel(row, lefCol)
# ~ Right ~
for row in range(1, nbRows - 1):
    process_pixel(row, rigCol)

# We validate all neighbours for all pixels in corners and edges because:
#   1) In an image of N pixels, there are 4 corners and ~4√(N) pixels part of
#       an edge, so optimizing the validations wouldn't do much anyway.
#   2) However, optimizing the validations will add a *lot* of complexity
#       to the code, because now you need to anticipate images of size...
#       (W is Width and H is Height)
#       - 1 × 1
#       - 2 × 2
#       - 2 × H
#       - W × 2
#       - 1 × H
#       - W × 1
#       And all the other weird cases I haven't thought of yet.
#   3) If instead of optimizing, you keep all the checks, then you *know* that
#       whatever the dimensions, the program will *not* try to access out-of-
#       bound indexes.
#
#   Will an image of 2×4096 have worse performances than expected? Yes.
#   Is that use-case a priority? No.
#   Will we still output a *correct* result for a 2×4096? *Yes.*


# ~~~ Center ~~~

all_pixels = image_asColour[1:maxRow-1, 1:maxColumn-1]

def batch_process(rowOffset, colOffset):
    firsRow = 1 + rowOffset
    lastRow = maxRow-1 + rowOffset
    firsCol = 1 + colOffset
    lastCol = maxColumn-1 + colOffset
    all_neighs = image_asColour[firsRow:lastRow, firsCol:lastCol]

    diffs = all_pixels != all_neighs
    diff_pixels = all_pixels[diffs]
    diff_neighs = all_neighs[diffs]

    for pair in zip(diff_pixels, diff_neighs):
        pixelColour = pair[0]
        neighColour = pair[1]
        adjacencies.setdefault(pixelColour, set()).add(neighColour)
        adjacencies.setdefault(neighColour, set()).add(pixelColour)

    return

batch_process(TOP_OFFSET, RIG_OFFSET)
batch_process(0, RIG_OFFSET)
batch_process(BOT_OFFSET, RIG_OFFSET)
batch_process(BOT_OFFSET, 0)

# ##### SORT #####



# ##### STRINGIFY #####



# ##### WRITE #####



# ##### OUTPUT #####
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
    
    adjacencies_as_tuple = dict()
    for pixel in adjacencies.keys():
        pixel_tuple = RGBA_from_uintc(pixel)
        adjacencies_as_tuple[pixel_tuple] = set()
        for neigh in adjacencies[pixel]:
            neigh_tuple = RGBA_from_uintc(neigh)
            adjacencies_as_tuple[pixel_tuple].add(neigh_tuple)

    sortedAdjacencies = [header]
    sortedPixels = sorted(adjacencies_as_tuple.keys())
    for pixel in sortedPixels:
        neighboursAsSet = adjacencies_as_tuple[pixel]
        sortedNeighbours = sorted(list(neighboursAsSet))
        for neighbour in sortedNeighbours:
            sortedAdjacencies.append(COLUMN_SEPARATOR.join(map(str, pixel + neighbour)))
            
    # TSV specifications say that each line must end with EOL
    # https://www.iana.org/assignments/media-types/text/tab-separated-values
    joinedAdjacencies = "\n".join(sortedAdjacencies)
    conformToTsvSpecifications = joinedAdjacencies + "\n"
    return conformToTsvSpecifications

stringyfied = stringify()

destination.write(stringyfied)

# ##### EPILOGUE #####
endTime = time.perf_counter()
executionDuration = round(endTime - startTime, 6)

logging.info("Finished in {:.3} seconds".format(executionDuration))

if args.profile:
    print("{}".format(executionDuration), file=sys.stderr)

