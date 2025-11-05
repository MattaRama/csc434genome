# CSC434: Human Genome Project 

## Introduction

This is a project I built for CSC434: AI & Machine Learning at SUNY Brockport.
In the specifications for the project, we are supposed to choose two chromosomes to
perform our analysis and search on. However, I decided that it would not be much
more difficult to perform my analysis and search on chromosomes 1-22 provided by
[this UCSC repository](https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/).

In order to make that possible, some optimizations had to be made. If running this
project, it is recommended that you have at least 8GB of free RAM and a somewhat
modern CPU. This project also downloads slightly less than 3GB of data into the
project directory.

This project was made and tested in Python 3.9.4, but any modern version of python
should do.

The project is composed of three primary parts:

### 1. Fetching and Preparing Data:
- DNA sequences for chromosomes 1-22 are downloaded locally, unzipped,
and stored for analysis and searching.

### 2. Chromosome Entropy and Statistics:
- Calculating the following attributes for each chromosome:
    - Total Length
    - Known Length (Length - unknown/N)
    - Total Occurrences (of each nucleotide and unknown/N)
    - GC Content
    - Known GC Content (ignore N when calculating)
    - Total Entropy
    - Known Entropy (ignore N when calculating)
    - Percentage Composition (of each nucleotide and unknown/N)
    - Known Percentage Composition (of each nucleotide)

### 2. Motif Search Algorithm (not yet started)
- Proposing and implementing a search algorithm to identify occurrences of a short
DNA pattern (motif) in a chromosome sequence.

## Setup
1. Clone the repository
    ```
    git clone <repository-url>
    cd <project-directory>
    ```

2. Create and activate a virtual environment
    ```
    python -m venv venv
    source venv/bin/activate
    ```
    Note: For Windows users, instead of `source venv/bin/activate`, run:
    ```
    venv\Scripts\activate
    ```

3. Install required dependencies in virtual environment
    ```
    pip install -r requirements.txt
    ```

## Usage

The chromosome data can be fetched using the `fetch-data.py` script, which should
be executed as such:
```
python src/fetch-data.py
```
This will download and decompress the chromosome data from the UCSC repository
into the `data/raw/` directory. Note that this requires that you have at least
2.75GB of available disk space.

Once you have downloaded the data, you can calculate the entropy and statistics
for each chromosome using:
```
python src/calc-stats.py
```
Due to the fact that synchronously calculating all 22 chromosomes would take a
somewhat significant amount of time, the script uses Python's multiprocessing 
module in order to run multiple analysis tasks at once. If you are on a lower-power
computer, you may choose to disable this feature and compute synchronously by
switching the `MULTIPROCESS_ENABLED` constant to `False`. You may also reduce the
CPU/RAM requirements of multiprocessing by reducing the `PROCESS_COUNT`, which
will limit the amount of tasks that `calc-stats.py` attempts to run at once.

The results of this analysis are both outputted to the console as well as to 
`out/statistics.json`, where you can review them or use them in another script for
further analysis.