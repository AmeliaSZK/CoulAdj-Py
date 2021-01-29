# Test samples

This file describes the features of the test samples distributed with this repo.
"Test samples" are images created specifically to test CoulAdj.
"Production samples" are images from the "real world" for which CoulAdj was created to analyze.

# Rules

Each test samples obey these rules:
1. Width and height are different.
1. Values in the red channel must be either 10 or 210
1. Values in the green channel must be either 20 or 220
1. Values in the blue channel must be either 30 or 230
1. Values in the alpha channel (if present) must be between 240 and 254 (inclusive).
Additionally, the alpha value must represent a unique RGB combination.
1. More specifically, only these colours are allowed:
    |   r |   g |   b |   a | Name       | Id |
    |-----|-----|-----|-----|------------|----|
    |  10 |  20 | 230 | 252 | Blue       | 12 |
    |  10 | 220 |  30 | 250 | Green      | 10 |
    |  10 | 220 | 230 | 248 | Cyan       |  8 |
    | 210 |  20 |  30 | 246 | Red        |  6 |
    | 210 |  20 | 230 | 244 | Magenta    |  4 |
    | 210 | 220 |  30 | 242 | Yellow     |  2 |
1. When looking at the image from top-left to top-right, from top to bottom,
the colours must appear such that those with the lower alpha values appear first.

## Hex values
|   r |   g |   b |   a | Name       | Id |
|-----|-----|-----|-----|------------|----|
|  0a |  14 |  e6 |  fc | Blue       | 12 |
|  0a |  dc |  1e |  fa | Green      | 10 |
|  0a |  dc |  e6 |  f8 | Cyan       |  8 |
|  d2 |  14 |  1e |  f6 | Red        |  6 |
|  d2 |  14 |  e6 |  f4 | Magenta    |  4 |
|  d2 |  dc |  1e |  f2 | Yellow     |  2 |

Use `$ hexdump filename` on Linux.

# Rationale

The rules regarding what colour is allowed were designed to accomplish these goals:

## Correct ordering of RGBA columns

The old test samples all had values of either 0 or 255. This complicated verifying
that the program had correctly identified the RGBA channels. 

Now, you can tell to which channel a value belongs by looking at the 2nd digit of
the value. If it's 1 (10 or 210), then red. 2 is green, 3 is blue, and 4 & 5 are alpha.

This is the same order the columns should be appearing in the output, and also the
same order that must be used to sort the colours.

## Quick identification of what colour a pixel should be.

Since the alpha value is unique for each pixel, we only need to look at the alpha
to know which colour is supposed to be represented by this pixel.

Before, we had to order and compare the 0s and 255s from all 3 RGB channels.

## Correct sorting of colours

We want the sort to be done by channels. ie, (10, 20, 230) must appear (in the ouput)
before (10, 220, 30). This is why we only encoded the ID of the colour in the alpha
channel. Had we encoded all the channels, the two colours would then be something
like (16, 26, 236) and (15, 225, 35), making that specifications unverifiable.

Furthermore, the IDs to encode in the alpha channel were chosen so that if the
output had been sorted, the alpha channel would also be sorted.

However, we didn't want this encoding to have an impact on the sorting itself,
so the IDs were chosen so that the alpha column should always be sorted from 
greater to lower value. This way, if the alpha was ever used to sort 2 colours,
it would be visible in the ouput.

## A sort was actually performed

Some languages use structures that remember the order of insertion. To verify
that the output was actually sorted and isn't depending on the insertion order,
the images are made so that the insertion order would give an obviously incorrect
result, because it would interfere with the expected ordering of the alpha column.

# Rules of thumb

When looking at the output...
* In each row, the digit of the tens should always be increasing from left column to right column
* In the alpha column, each row should have a value greater or equal than the row below.