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
#       From that sorted list, craft the string to write in the TSV file
#
#   5) Write
#       Take that string, and write it to the TSV file
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

def gre_from_RGBA(rgba):
    return rgba[1]

def blu_from_RGBA(rgba):
    return rgba[2]

def alp_from_RGBA(rgba):
    return rgba[3]



# ##### INPUTS #####
source = args.image
destination = args.results
relateDiagonals = not args.dontRelateDiagonals
logging.info("Starting")

# ##### IMPORT #####
source_image = imageio.imread(source)
height = source_image.shape[0]
width = source_image.shape[1]
nbChannels = source_image.shape[2]
logging.debug("source_image.shape = {}".format(source_image.shape))
logging.info("Height = {}, Width = {}, {} channels".format(height, width, nbChannels))

nbRows = height
nbCols = width
maxRow = nbRows - 1
maxCol = nbCols -1
logging.debug("nbRows={}, nbColumns={}, maxRow={}, maxColumn={}"
    .format(nbRows, nbCols, maxRow, maxCol))
topRow = 0
botRow = maxRow
lefCol = 0
rigCol = maxCol
logging.debug("topRow={}, botRow={}, lefCol={}, rigCol={}"
    .format(topRow, botRow, lefCol, rigCol))

start_apply = time.perf_counter()
image = np.apply_along_axis(colourKey_from_pixelData, 2, source_image)
end_apply = time.perf_counter()
duration_apply = round(end_apply - start_apply, 3)
logging.debug("image.shape = {}".format(image.shape))
logging.debug(f"Time spent converting the array: {duration_apply}s")

# ##### CALCULATE ADJACENCIES #####
adjacencies = dict()

def batch_process(all_pixels, all_neighs):
    diffs = all_pixels != all_neighs
    diff_pixels = all_pixels[diffs]
    diff_neighs = all_neighs[diffs]

    for pair in zip(diff_pixels, diff_neighs):
        pixelColour = pair[0]
        neighColour = pair[1]
        adjacencies.setdefault(pixelColour, set()).add(neighColour)
        adjacencies.setdefault(neighColour, set()).add(pixelColour)

    return

bot_pixels = image[0:-1, :]
bot_neighs = image[1:  , :]

rig_pixels = image[:, 0:-1]
rig_neighs = image[:, 1:]

bot_rig_pixels = image[0:-1, 0:-1]
bot_rig_neighs = image[1:  , 1:]

top_rig_pixels = image[1:  , 0:-1]
top_rig_neighs = image[0:-1, 1:]

logging.debug("bot_pixels.shape = {}".format(bot_pixels.shape))
logging.debug("bot_neighs.shape = {}".format(bot_neighs.shape))
logging.debug("rig_pixels.shape = {}".format(rig_pixels.shape))
logging.debug("rig_neighs.shape = {}".format(rig_neighs.shape))
logging.debug("bot_rig_pixels.shape = {}".format(bot_rig_pixels.shape))
logging.debug("bot_rig_neighs.shape = {}".format(bot_rig_neighs.shape))
logging.debug("top_rig_pixels.shape = {}".format(top_rig_pixels.shape))
logging.debug("top_rig_neighs.shape = {}".format(top_rig_neighs.shape))

batch_process(bot_pixels, bot_neighs)
batch_process(rig_pixels, rig_neighs)
if relateDiagonals:
    batch_process(bot_rig_pixels, bot_rig_neighs)
    batch_process(top_rig_pixels, top_rig_neighs)

# ##### SORT #####
def sort_adjacencies(adjacencies: dict) -> list:
    unsorted_adjacencies = list()

    for this_colour_key, all_adjacents in adjacencies.items():
        colour_RGBA = RGBA_from_colourKey(this_colour_key)

        for this_adjacent_key in all_adjacents:
            adjacent_RGBA = RGBA_from_colourKey(this_adjacent_key)

            this_relation = relation_from_two_RGBAs(colour_RGBA, adjacent_RGBA)
            unsorted_adjacencies.append(this_relation)

    return sorted(unsorted_adjacencies)

sorted_adjacencies = sort_adjacencies(adjacencies)

# ##### STRINGIFY #####
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

def stringify(sorted_adjacencies):
    #nbChannels = image.shape[2]
    HARDCODED_RGBALPHA = 4
    nbChannels = HARDCODED_RGBALPHA
    if nbChannels == 3:
        header = HEADERS["RGB"]
    elif nbChannels == 4:
        header = HEADERS["RGB_ALPHA"]
    else:
        raise TypeError("Image must have 3 or 4 channels")
    
    all_lines = list()
    all_lines.append(header)
    for relation in sorted_adjacencies:
        colour_RGBA = colour_RGBA_from_relation(relation)
        adjcnt_RGBA = adjacent_RGBA_from_relation(relation)
        r = red_from_RGBA(colour_RGBA)
        g = gre_from_RGBA(colour_RGBA)
        b = blu_from_RGBA(colour_RGBA)
        a = alp_from_RGBA(colour_RGBA)
        adj_r = red_from_RGBA(adjcnt_RGBA)
        adj_g = gre_from_RGBA(adjcnt_RGBA)
        adj_b = blu_from_RGBA(adjcnt_RGBA)
        adj_a = alp_from_RGBA(adjcnt_RGBA)
        channels = [r, g, b, a, adj_r, adj_g, adj_b, adj_a]
        joined_channels = COLUMN_SEPARATOR.join(map(str, channels))
        all_lines.append(joined_channels)
            
    # TSV specifications say that each line must end with EOL
    # https://www.iana.org/assignments/media-types/text/tab-separated-values
    joined_lines = "\n".join(all_lines)
    conform_to_tsv_specifications = joined_lines + "\n"
    return conform_to_tsv_specifications

stringyfied = stringify(sorted_adjacencies)

# ##### WRITE #####
destination.write(stringyfied)

# ##### EPILOGUE #####
endTime = time.perf_counter()
executionDuration = round(endTime - startTime, 6)

logging.info("Finished in {:.3} seconds".format(executionDuration))

if args.profile:
    print("{}".format(executionDuration), file=sys.stderr)

