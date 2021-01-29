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
conda env create -f environment.yml
```

## To Run
1. Read these instructions
1. Take a quick look at the source code to see if they still make sense (sorry 😅)
1. While you're in the source code, modify the input variables at the
top of the file to suit what you want to run in the program (Gotcha 😎)
1. On the command line, navigate to the cloned repository
1. Run these commands:
    ```
    conda activate CoulAdj-Py
    python CoulAdj-Py.py
    ```

## How to update Anaconda environment
During development, more packages may need to be added to the Anaconda environment.
This is how you can update it, when you are already in the CoulAdj-Py environment:

1. Modify the environment.yml file to include the package to add
1. Execute these commands in the terminal:
    ```
    (CoulAdj-Py) $ conda deactivate
    (base) $ conda env update -f environment.yml
    (base) $ conda activate CoulAdj-Py
    (CoulAdj-Py) $
    ```
    In these instructions, the `(CoulAdj-Py)` and `(base)` are inserted by
    Anaconda in your terminal to signal which environment is currently active.
    The `$` represents your terminal prompt.


# API

## Input 
*   Source image file path
*   Source image Python file object (maybe?)
*   Option(s)
    * Relate Diagonals
        * `True` by default. All 8 neighbours are considered adjacent.
        * If `False`, only consider as adjacent the four (4) neighbours with
        a common edge. (top, bottom, left, and right neighbours)

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