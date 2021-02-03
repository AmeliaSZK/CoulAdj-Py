# Colour Adjacencies
Reads an image and outputs the colour adjacencies.

Primary objective is to help me learn Python. 

This project declares conformity to [SemVer 2.0.0](https://semver.org/spec/v2.0.0.html).
There is currently no API version number, because there has been no public release.

**This project is still in development and is not ready for public consumption.**

"Colour" and "color" will be used interchangeably and arbitrarily in both the code
and documentation.

Long term objective is to publish as a module on PIP.

# About this Github repository

*   I made this Github repository public so I could share with my twitter friends.
*   It may be made private in the future.

# Known or Assumed Requirements

* [Anaconda](https://www.anaconda.com/products/individual)
    * Development was done with the Individual Edition (Distribution)
    * _NB: Upon install, Anaconda will modify your command line prompt to prefix
        it with the active environment in parenthesis._

# How to run

**NB: These instructions have not been tested on Windows**

## First time setup
1. Clone the git repository
1. On the command line, navigate to the cloned repository
1. Run this command:
    ```
    $ conda env create -f environment.yml
    ```

## To Run
1. On the command line, navigate to the cloned repository
1. Activate the Anaconda environment:
    ```
    $ conda activate CoulAdj-Py
    (CoulAdj-Py) $
    ```
1. Run the program:
    ```
    (CoulAdj-Py) $ python CoulAdj-Py.py path/to/image.png path/to/results.tsv
    ```

To get the full command line usage help message:
```
(CoulAdj-Py) $ python CoulAdj-Py.py -h
usage: CoulAdj-Py.py [-h] [-d] [-v] [-n] [-p] image results

Computes, for each colour in the image, the list of all adjacent colours and writes the results to a TSV file.

positional arguments:
  image                 The image file to process.
  results               The TSV file in which to write the results. 
                        If it already exists, it will be erased and overwritten.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dont-relate-diagonals
                        if present, will only consider the 4 neighbours with a 
                        common edge (top, bottom, left, right) to be adjacent.
                        By default, all 8 neighbours are considered adjacent
  -v, --verbose         displays information about the file and the computations
  -n, --version         show program's version number and exit
  -p, --profile         (for developers; users should use -v instead) 
                        Prints the execution time to stderr
                        regardless of logging level

CoulAdj-Py Copyright (C) 2021 Amélia SZK. Released under GPL-3.0 License.
```
*(This example may not be up-to-date)*

Regardless of wether or not the above example is up-to-date, these
characteristics of the command line interface are *not* subject to change:
* The last argument is the results file.
* The second-to-last argument is the image file.
* The `--dont-relate-diagonals` flag will enable the `dont-relate-diagonals` option.

## Tests
There are two tests you can run: correctness and performance.

### Correctness



# API

## Input 
*   Source image file path
*   Destination file path
*   Option(s)
    * `dont-relate-diagonals`
        * If present, only consider as adjacent the four (4) neighbours with
        a common edge. (top, bottom, left, and right neighbours)
        * By default, all 8 neighbours are considered adjacent.

## Known limitations
*   (none yet)


## Output
*   TSV File
*   Python native object (maybe?)

### TSV File
*   Tab-separated values (tsv)
    *   [Summary on Wikipedia](https://en.wikipedia.org/wiki/Tab-separated_values) 
    *   [Official specifications](https://www.iana.org/assignments/media-types/text/tab-separated-values)

*   Data will be organized like this:

    |r  |g  |b  |a  |adj_r|adj_g|adj_b|adj_a|
    |---|---|---|---|-----|-----|-----|-----|
    |0  |32 |64 |128|0    |0    |0    |255  |
    |0  |32 |64 |255|0    |0    |0    |255  |
    |0  |32 |64 |255|0    |32   |0    |255  |
    |0  |64 |0  |255|0    |0    |0    |255  |

*   The alpha column will always be included in the output. Images without an alpha channel
will get an alpha value at full opacity.

    |r  |g  |b  |a  |adj_r|adj_g|adj_b|adj_a|
    |---|---|---|---|-----|-----|-----|-----|
    |0  |32 |64 |255|0    |0    |0    |255  |
    |0  |32 |64 |255|0    |32   |0    |255  |
    |0  |64 |0  |255|0    |0    |0    |255  |


*   The rows will be sorted in ascending order.

    |r  |g  |b  |a  |adj_r|adj_g|adj_b|adj_a|
    |---|---|---|---|-----|-----|-----|-----|
    |0  |32 |64 |255|0    |0    |0    |255  |
    |0  |32 |64 |255|0    |32   |0    |255  |
    |0  |32 |64 |255|0    |128  |0    |255  |
    |0  |64 |0  |255|0    |0    |0    |255  |
    |32 |0  |0  |255|0    |0    |0    |255  |
    |255|0  |0  |255|0    |0    |0    |255  |

*   Symmetric relations will be included;
if A is adjacent to B, then B is adjacent to A, 
so this single relation will generate two rows.

    |r  |g  |b  |a  |adj_r|adj_g|adj_b|adj_a|
    |---|---|---|---|-----|-----|-----|-----|
    |0  |0  |0  |255|0    |64   |0    |255  |
    |0  |64 |0  |255|0    |0    |0    |255  |

*   Reflexive relations will *not* be included;
a color cannot be adjacent with itself.

*   Colors that differ only in their alpha value are considered distinct.

    |r  |g  |b  |a  |adj_r|adj_g|adj_b|adj_a|
    |---|---|---|---|-----|-----|-----|-----|
    |0  |0  |0  |128|0    |0    |0    |255  |
    |0  |0  |0  |255|0    |0    |0    |128  |

*   Columns will appear in this order:
    - Red
    - Green
    - Blue
    - Alpha
    - Adjacent Red
    - Adjacent Green
    - Adjacent Blue
    - Adjacent Alpha

*   The first row will contain the column names.
*   The column names will be:

    |Column Name|Color Channel  |
    |-----------|---------------|
    | `r`       |Red            |
    | `g`       |Green          |
    | `b`       |Blue           |
    | `a`       |Alpha          |
    | `adj_r`   |Adjacent Red   |
    | `adj_g`   |Adjacent Green |
    | `adj_b`   |Adjacent Blue  |
    | `adj_a`   |Adjacent Alpha |

*   The line-endings may be either in Windows (CRLF) or Unix (LF) style.

### Python Native Object
(To be completed)