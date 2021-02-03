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

version = "0.1"

# ~~~~~ Prologue ~~~~~

# ~~~ Profiling ~~~
startTime = time.perf_counter()

# ~~~ Command Line Interface ~~~
diags_flags = ("-d", "--dont-relate-diagonals")
verbose_flags = ("-v", "--verbose")
profile_flags = ("-p", "--profile")
version_flags = ("-n", "--version")

description_program = "Computes, for each colour in the image," \
    " the list of all adjacent colours and writes the results to a TSV file."
epilog_program = "CoulAdj-Py  Copyright (C) 2021  Amélia SZK." \
    "\nReleased under GPL-3.0 License."

help_diags = "if present, will only consider the 4 neighbours with a common edge" \
    " (top, bottom, left, right) to be adjacent." \
    " By default, all 8 neighbours are considered adjacent"
help_verbose = "displays information about the file and the computations"
help_profile = "(for developers; users should use {} instead)" \
    " Prints the execution time to stderr regardless of logging level".format(verbose_flags[0])
help_img = "The image file to process."
help_res = "The TSV file in which to write the results. " \
    "If it already exists, it will be erased and overwritten."

parser = argparse.ArgumentParser(description=description_program, epilog=epilog_program)
parser.add_argument(*diags_flags, help=help_diags,
    action="store_true", dest="dontRelateDiagonals")
parser.add_argument(*verbose_flags, help=help_verbose,
    action="store_true")
parser.add_argument(*version_flags, 
    action="version", version="%(prog)s " + version)
parser.add_argument(*profile_flags, help=help_profile,
    action="store_true")
parser.add_argument("image", help=help_img, 
    type=argparse.FileType("rb"))
parser.add_argument("results", help=help_res, 
    type=argparse.FileType("w"))
args = parser.parse_args()

exit()
# ~~~ Logging ~~~

# # Input

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

source = args.image
destination = args.results
relateDiagonals = not args.dontRelateDiagonals
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
    neighColumn = pixelColumn + columnOffset
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

destination.write(stringyfied)

# Report execution duration
endTime = time.perf_counter()
executionDuration = round(endTime - startTime, 3)
print("{}".format(executionDuration))
