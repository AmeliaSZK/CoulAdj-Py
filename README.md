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
usage: CoulAdj-Py.py [-h] [-d] [-v] [-n] image results

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
  -v, --verbose         display informations about the file and the computations
  -n, --version         show program's version number and exit

CoulAdj-Py Copyright (C) 2021 Amélia SZK. Released under GPL-3.0 License.
```
*(This example may not be up-to-date)*

Regardless of wether or not the above example is up-to-date, these
characteristics of the command line interface are *not* subject to change:
* The last argument is the results file.
* The second-to-last argument is the image file.
* The `--dont-relate-diagonals` flag will enable the `--dont-relate-diagonals` option.

# Tests
There are four tests you can run: 
* Correctness
* Duration
* Temporal Complexity
* Profile of all sizes

The following notes apply to all tests:
* Run the commands from the root of the repository
* All scripts, unless noted, verify that results are correct
    * Failures are notified, and successes are not
* To understand the concept of "size", refer to the 
[test samples Readme](tests/README.md)
    * More specifically, you need to read the `Size` section of
    that document
    * The sections before `Size` are a general introduction, 
    and are probably helpful to also read.
    * The sections after `Size` will become helpful if you need to debug 
    incorrect results; they aren't required reading to understand the test scripts.
* The scripts should print, at the end, instructions on how to interpret 
and/or use the results.
* In script results, **all durations are given in seconds**
* Durations are printed by the program (not the test script) on stderr
* In this Readme, the **commands are kept up-to-date**
* In this Readme, the **results given in examples may be outdated**


## Correctness
Run with `(CoulAdj-Py) $ bash test-correctness.sh`

Used to quickly make sure the program gives correct results.

Will run the program on small sample sizes and report when finished.
Will also report all failing tests.


### Good
```
(CoulAdj-Py) $ bash test-correctness.sh
~~~ Testing correctness at sizes 1 and 8 ~~~
~~~ Correctness test finished ~~~
If no failure was reported, then all were correct.
(CoulAdj-Py) $
```

### Bad
```
(CoulAdj-Py) $ bash test-correctness.sh
~~~ Testing correctness at sizes 1 and 8 ~~~
Size 1 failed
Size 8 failed
~~~ Correctness test finished ~~~
If no failure was reported, then all were correct.
(CoulAdj-Py) $
```

### Weird
```
(CoulAdj-Py) $ bash test-correctness.sh
~~~ Testing correctness at sizes 1 and 8 ~~~
Size 1 failed
~~~ Correctness test finished ~~~
If no failure was reported, then all were correct.
(CoulAdj-Py) $
```
This is weird because the script says it tests sizes 1 and 8, 
but only size 1 failed. If a size fails, all others should fail.

Start by checking that the script isn't lying about the sizes under test.

_(Yes, that pretty header is just a static string lol, sorry not sorry)
(Look, designing and tuning test scripts is long, and bash is hard to 
write and learn, okay?_ 😩 )


## Duration
Run with `(CoulAdj-Py) $ bash test-duration.sh`

Used to compare how useful a particular optimization was.

For each size under test, will execute several runs and display the duration
for each individual run. 
These durations are meant to be averaged before comparing between optimizations.

### Protocol
1. Run `(CoulAdj-Py) $ bash test-duration.sh`
1. Copy the results in a spreadsheet
1. In the spreadsheet, calculate the average
1. Round this average to 3 digits
1. Report the rounded number as the performance of this commit:
    1. Add an entry in [durations.tsv](durations.tsv)
    1. Include the duration in the commit short message

### Example
```
(CoulAdj-Py) $ bash test-duration.sh
~~~ Starting performance test ~~~
~ Size 16 ~ (10 runs)
0.495205
0.487364
0.515644
0.525737
0.542067
0.511323
0.518518
0.502498
0.511994
0.494947
~~~ Performance test finished ~~~
To calculate the performance of a size:
  1) Average all durations for that size
  2) Round this average to 3 digits
  3) That's it :)
(CoulAdj-Py) $
```
Average: `0.5045312`

Rounded: `0.505`

## Temporal Complexity
Run with `(CoulAdj-Py) $ bash test-temporal-complexity.sh`

Used to quickly evaluate the temporal complexity (Big O) of the program.

Will test a few small consecutive sizes, with only one run per size.

* **The program should be `O(n)`**
* If you have more than that, bring it down to O(n) before profiling all sizes
* If you have less, I expect one of these to be true:
    * The test script(s) and/or program is very broken 😶
    * You're a genius, please please please tell me how you did it 👀 🎉
* **At `O(n)`, each size takes about 4 times longer than the previous size**

```
(CoulAdj-Py) $ bash test-temporal-complexity.sh
~~~ Profiling Sizes 8 to 64 ~~~
Expect 6~12 seconds to do size 64
Size 8: 0.150215
Size 16: 0.503862
Size 32: 1.969428
Size 64: 7.50256
~~~ Temporal complexity test finished ~~~
At O(n), each size takes ~4x longer than the previous.
Actual ratios have ranged from 3.4x to 4.2x
(CoulAdj-Py) $ 
```

## Profile of All Sizes
Run with `(CoulAdj-Py) $ bash profile-all-sizes.sh`

Used to compare performance between milestones in the project, or between
different implementations of CoulAdj.

Before running this script, make sure your temporal complexity is less than
or equal to `O(n)`.

Works like the Temporal Complexity test, but on a much wider range of sizes.

Write your results in [all_sizes.tsv](all_sizes.tsv).

### Protocol
1. Run `(CoulAdj-Py) $ bash profile-all-sizes.sh`
1. Follow instructions

The protocol is kept short because:
1. Formally documenting it would be long tedious
1. I'm not sure a full documentation would be useful
1. The test protocols are still subject to changes, and keeping the Readme
updated is always so, so long
1. This particular script was created because I thought that 
"surely it's gonna be useful", not because I saw an actual and immediate need
1. For real, it's just the Temporal Complexity with more sizes and a dedicated
TSV file to keep track of the results. (And a supporting spreadsheet... 😅)

### Example
```
(CoulAdj-Py) $ bash profile-all-sizes.sh
~~~ Profiling Sizes 1 to 512 ~~~
Expect up to 6~12 minutes in total. (It's 10~11 on my machine)
Each size should take ~4x longer than the previous.
Size 1: 0.036352
Size 2: 0.041543
Size 4: 0.06418
Size 8: 0.154275
Size 16: 0.485168
Size 32: 1.921757
Size 64: 7.962166
Size 128: 32.105543
Size 256: 125.074073
Size 512: 523.067901
~~~ Profiling of all sizes finished ~~~
Truncate durations to 4 digits before calculating & recording ratios.
  "Truncate to 4 digits" will give you 5 chars bc of the decimal point.
  "Recording ratios" means to write them in all_sizes.tsv
(CoulAdj-Py) $
```

### Calculation example
With the example above, how you would calculate what to record in `all_sizes.tsv`:
1. Duration of size 256 is `125.074073`
1. Duration of size 512 is `523.067901`
1. Recorded duration of 256 is `125.0`
1. Recorded duration of 512 is `523.0`
1. `523.0` divided by `125.0` equals `4.184`
1. Recorded ratio for 512 is `4.18`
1. Write the ratio as `4.18x` so it's not mistaken for a duration
1. I don't think it matters if you round or truncate to get from `4.184` to `4.18`

### (Probably) Outdated protocol

Will run a few samples of different sizes. Check the source of `test-perf.sh`
to see which sizes are activated. ("activated" means "not commented")

Execution time of each sample will be printed.
Failing tests will be signaled.
Completion of all tests will also be reported.

### Good
```
(CoulAdj-Py) $ bash test-perf.sh
Size 128: 0.692
Size 256: 2.73
Performance test finished
```
Notice that doubling the size quadrupled the execution time.
This is expected, because when the size doubles, the number of pixels quadruples.
It means the implementation is O(n).

Also, the size closest to the intended input is 512. 
4 times 2.73s is 10.92s, which is a good (but not excellent) execution time.

### Okay
```
(CoulAdj-Py) $ bash test-perf.sh
Size 16: 0.702
Size 32: 2.71
Size 64: 10.9
Size 128: 43.1
Performance test finished
```
The actual performance at the time of writing these lines.
It's definitely not good, because at these rates, the size 512 will take
11 minutes to complete. 

It is, however, not *bad*, because since execution time is still quadrupling,
we are still in O(n).

### Bad
```
(CoulAdj-Py) $ bash test-perf.sh
Size 16: 0.692
Size 32: 5.5
Performance test finished
```
The implementation under test is O(n²), and the intended use-case has an `n` of 13M... 😶

### Unacceptable
```
(CoulAdj-Py) $ bash test-perf.sh
Size 128: 0.692
Size 128 failed
Size 256: 2.73
Size 256 failed
Performance test finished
```
A program can be so slow that it becomes useless, but an incorrect program
is worse than useless. 


# API

## Input 
*   Source image file path
*   Destination file path
*   Option(s)
    * `--dont-relate-diagonals`
        * If present, only consider as adjacent the four (4) neighbours with
        a common edge. (top, bottom, left, and right neighbours)
        * By default, all 8 neighbours are considered adjacent.

## Known limitations
*   (none yet)


## Output
*   TSV File

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
