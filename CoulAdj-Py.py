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

# ~~~~~ Prologue ~~~~~
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
epilog_program = "CoulAdj-Py  Copyright (C) 2021  Amélia SZK." \
    "\nReleased under GPL-3.0 License."

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

# ~~~~~ Constants ~~~~~
TOP_OFFSET = -1
BOT_OFFSET = 1
LEF_OFFSET = -1
RIG_OFFSET = 1

# ~~~~~ Inputs ~~~~~
source = args.image
destination = args.results
relateDiagonals = not args.dontRelateDiagonals
logging.info("Starting")

# ~~~~~ Processing ~~~~~
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


def process_pixel(pixelRow, pixelColumn):
    pixelColour = tuple(image[pixelRow, pixelColumn].tolist())
    #process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, RIG_OFFSET)
    #process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, LEF_OFFSET)
    process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, RIG_OFFSET)
    if relateDiagonals:
        process_neighbour(pixelColour, pixelRow, pixelColumn, BOT_OFFSET, 0)
        process_neighbour(pixelColour, pixelRow, pixelColumn, 0, RIG_OFFSET)
        #process_neighbour(pixelColour, pixelRow, pixelColumn, 0, LEF_OFFSET)
        #process_neighbour(pixelColour, pixelRow, pixelColumn, TOP_OFFSET, 0)

        
def process_neighbour(pixelColour, pixelRow, pixelColumn, rowOffset, columnOffset):
    neighRow = pixelRow + rowOffset
    neighColumn = pixelColumn + columnOffset
    if not valid_row_column(neighRow, neighColumn): 
        return
    neighColour = tuple(image[neighRow, neighColumn].tolist())
    if same_colours(pixelColour, neighColour): 
        return
    adjacencies.setdefault(pixelColour, set()).add(neighColour)
    adjacencies.setdefault(neighColour, set()).add(pixelColour)
    
    
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


# ~~~ Center ~~~
for row in range(1, nbRows - 1):
    for column in range(1, nbColumns - 1):
        process_pixel(row, column)


# ~~~~~ Output ~~~~~
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
            
    # TSV specifications say that each line must end with EOL
    # https://www.iana.org/assignments/media-types/text/tab-separated-values
    joinedAdjacencies = "\n".join(sortedAdjacencies)
    conformToTsvSpecifications = joinedAdjacencies + "\n"
    return conformToTsvSpecifications

stringyfied = stringify()

destination.write(stringyfied)

# ~~~~~ Epilogue ~~~~~
endTime = time.perf_counter()
executionDuration = round(endTime - startTime, 6)

logging.info("Finished in {:.3} seconds".format(executionDuration))

if args.profile:
    print("{}".format(executionDuration), file=sys.stderr)

