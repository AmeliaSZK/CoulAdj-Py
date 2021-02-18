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
import concurrent.futures

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
#       From that 2D array, construct a set of `relations`
#
#   3) Sort
#       From that set, construct a sorted list of `relations`
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
# Furthermore, Import is responsible for assigning the correct functions
#   to colourKey_from_pixelData and RGBA_from_colourKey


def tuple_from_pixelData_rgbalpha(pixelData: np.ndarray):
    r = pixelData[0]
    g = pixelData[1]
    b = pixelData[2]
    a = pixelData[3]
    return (r, g, b, a)

def tuple_from_pixelData_rgb(pixelData: np.ndarray):
    r = pixelData[0]
    g = pixelData[1]
    b = pixelData[2]
    return (r, g, b)

def RGBA_from_rgbalpha_tuple(colourKey):
    r = colourKey[0]
    g = colourKey[1]
    b = colourKey[2]
    a = colourKey[3]
    return (r, g, b, a)

def RGBA_from_rgb_tuple(colourKey):
    r = colourKey[0]
    g = colourKey[1]
    b = colourKey[2]
    a = 255
    return (r, g, b, a)


# ~~~ BOUNDARY ~~~
def colourKey_from_pixelData(pixelData: np.ndarray):
    pass

def RGBA_from_colourKey(colourKey):
    pass

def relation_from_two_RGBAs(rgba1, rgba2):
    return (rgba1, rgba2)
# ~~~ BOUNDARY ~~~


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
image = imageio.imread(source)
height = image.shape[0]
width = image.shape[1]
nbChannels = image.shape[2]
pixelFormat = image.dtype
logging.debug("image.shape = {}".format(image.shape))
logging.info("Height: {}, Width: {}, {} channels, Pixel format: {}".format(height, width, nbChannels, pixelFormat))

# TODO:
# np.issubtype https://numpy.org/doc/stable/reference/generated/numpy.issubdtype.html#numpy.issubdtype
# Get maxes: https://numpy.org/doc/stable/reference/routines.dtype.html#data-type-information

if nbChannels == 3:
    colourKey_from_pixelData = tuple_from_pixelData_rgb
    RGBA_from_colourKey = RGBA_from_rgb_tuple
elif nbChannels == 4:
    colourKey_from_pixelData = tuple_from_pixelData_rgbalpha
    RGBA_from_colourKey = RGBA_from_rgbalpha_tuple
else:
    raise TypeError("Image must have 3 or 4 channels")

# ##### CALCULATE ADJACENCIES #####

def batch_process(all_pixels, all_neighs, batch_name=None):
    # Based on https://stackoverflow.com/a/50910650 by Jan Christoph Terasa
    # (with modifications)
    start = time.perf_counter()
    if batch_name is not None:
        batch_name = f'({batch_name})'
    else:
        batch_name = ''

    diffs = (all_pixels != all_neighs).any(axis=2)
    
    end_comp = time.perf_counter()
    
    diff_pixels = all_pixels[diffs]
    diff_neighs = all_neighs[diffs]
    
    end_list = time.perf_counter()

    zipped = np.hstack((diff_pixels, diff_neighs))
    # Example:
    # diff_pixels = [
    #   [1, 2, 3],
    #   [4, 5, 6],
    # ]
    # diff_neighs = [
    #   [ 7,  8,  9],
    #   [10, 11, 12],
    # ]
    # zipped = [
    #   [1, 2, 3,  7,  8,  9],
    #   [4, 5, 6, 10, 11, 12]
    # ]
    end_zipp = time.perf_counter()
    nb_zipp = zipped.size

    unique = np.unique(zipped, axis=0)

    end_uniq = time.perf_counter()
    nb_uniq = unique.size

    adjacencies = set()
    for pair in unique:
        pixelColour = RGBA_from_colourKey(pair[0:nbChannels])
        neighColour = RGBA_from_colourKey(pair[nbChannels:])
        adjacencies.add(relation_from_two_RGBAs(pixelColour, neighColour))
        adjacencies.add(relation_from_two_RGBAs(neighColour, pixelColour))
    
    end_register = time.perf_counter()
    nb_adja = len(adjacencies)

    duration_comp = round(end_comp - start, 4)
    duration_list = round(end_list - end_comp, 4)
    duration_zipp = round(end_zipp - end_list, 4)
    duration_uniq = round(end_uniq - end_zipp, 4)
    duration_regi = round(end_register - end_uniq, 4)
    duration_tot = round(end_register - start, 4)
    logging.debug(
        f"{duration_tot:0<6}s total."\
            f" Comparing: {duration_comp:0<6}"\
            f", Listing: {duration_list:0<6}"\
            f", Zipping: {duration_zipp:0<6}"\
            f", Purging: {duration_uniq:0<6}"\
            f", Registering: {duration_regi:0<6}." \
            f" {nb_zipp:,} zipped, {nb_uniq} uniques, {nb_adja} relations."\
            f" {batch_name}"
        )

    return adjacencies

all_adjacencies = set()

bot_pixels = image[0:-1, :]
bot_neighs = image[1:  , :]
rig_pixels = image[:, 0:-1]
rig_neighs = image[:, 1:]

bot_rig_pixels = image[0:-1, 0:-1]
bot_rig_neighs = image[1:  , 1:]
top_rig_pixels = image[1:  , 0:-1]
top_rig_neighs = image[0:-1, 1:]

start_process = time.perf_counter()

# with concurrent.futures.ThreadPoolExecutor() as executor:
#     results = [
#         executor.submit(batch_process, bot_pixels, bot_neighs, 'Bottom'),
#         executor.submit(batch_process, rig_pixels, rig_neighs, 'Right')
#     ]
#     if relateDiagonals:
#         results.append(executor.submit(batch_process, bot_rig_pixels, bot_rig_neighs, 'Bottom Right'))
#         results.append(executor.submit(batch_process, top_rig_pixels, top_rig_neighs, 'Top Right'))
    
#     end_setup = time.perf_counter()

#     duration_union = 0
#     for f in concurrent.futures.as_completed(results):
#         start_union = time.perf_counter()
        
#         all_adjacencies |= f.result()
        
#         end_union = time.perf_counter()
#         duration_union += (end_union - start_union)
    
#     end_join = time.perf_counter()

#     duration_setup = round(end_setup - start_process, 4)
#     duration_join = round(end_join - end_setup, 4)
#     duration_union = round(duration_union, 4)
#     logging.debug(f"Setup: {duration_setup}s, Join: {duration_join}s, Union: {duration_union}s")

adja_bot = batch_process(bot_pixels, bot_neighs, 'Bottom')
adja_rig = batch_process(rig_pixels, rig_neighs, 'Right')
if relateDiagonals:
    adja_bot_rig = batch_process(bot_rig_pixels, bot_rig_neighs, 'Bottom Right')
    adja_top_rig = batch_process(top_rig_pixels, top_rig_neighs, 'Top Right')
else:
    adja_bot_rig = set()
    adja_top_rig = set()

all_adjacencies |= adja_bot
all_adjacencies |= adja_rig
all_adjacencies |= adja_bot_rig
all_adjacencies |= adja_top_rig


end_process = time.perf_counter()
duration_process = round(end_process - start_process, 6)
logging.debug(f"Processing took {duration_process}s")

# ##### SORT #####
def sort_adjacencies(adjacencies: set) -> list:
    unsorted_adjacencies = list(adjacencies)
    return sorted(unsorted_adjacencies)

sorted_adjacencies = sort_adjacencies(all_adjacencies)

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
    header = HEADERS["RGB_ALPHA"]
    
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

