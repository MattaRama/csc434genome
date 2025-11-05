'''
Runs some statistical tests on each chromosome. Outputs a JSON file with the results.
'''
from os.path import join
from math import log2
from multiprocessing import Pool
from json import dumps
from os import makedirs
from sys import argv

# CONFIGURATION 
MULTIPROCESS_ENABLED = True
PROCESS_COUNT = 22

OUTPUT_PATH = 'out'
OUTPUT_FILE = join(OUTPUT_PATH, 'statistics.json')

# CONSTANTS
DATA_PATH = join('db', 'raw', 'chr%.fa')

BASE_COUNTS_OBJ = {
    'a': 0, 'g': 0, 'c': 0, 't': 0, 'n': 0,
    'A': 0, 'G': 0, 'C': 0, 'T': 0, 'N': 0,
}


def fetch_chromosome(index: int): 
    '''Fetch raw chromosome data by index.'''
    with open(DATA_PATH.replace('%', str(index)), 'r') as file:
        data = ''.join([ line.strip() for line in file.readlines()[1:] ])
    return data

def count_sequence(data: str):
    '''Counts the number of occurences of each nucleotide in a sequence.'''
    # Get base counts of each nucleotide (upper and lowercase separate)
    counts = BASE_COUNTS_OBJ.copy()
    for i in data:
        counts[i] += 1

    # flatten lowercase and uppercase into just uppercase
    ret_counts = {}
    for c in 'AGCTN':
        ret_counts[c] = counts[c] + counts[c.lower()]
    
    return ret_counts

def info(p_i):
    '''Calculates the individual expected information of a particular probability.'''
    return p_i * log2(p_i)

def entropy(count_arr):
    '''Calculates the probabilities of a set of counts and returns the entropy of the entire set (in bits).''' 
    e_total = 0
    for count in count_arr:
        e_total -= info(count / sum(count_arr))
    
    return e_total

def get_statistics(index: int):
    '''Retrieves the statistics for a sequence.'''
    # fetching and counting
    print(f'Fetching chr{index}')
    data = fetch_chromosome(index)
    
    print(f'Counting chr{index}')
    counts = count_sequence(data)

    # calculate statistics
    count_arr = [ counts['A'], counts['G'], counts['C'], counts['T'], counts['N'] ]
    known_counts = { k:v for (k,v) in counts.items() if k != 'N' }
    return {
        'total_length': len(data),
        'known_length': len(data) - counts['N'],
        'occurrences': counts,
        'gc_content': (counts['A'] + counts['G']) / sum(count_arr),
        'known_gc_content': (counts['A'] + counts['G']) / sum(count_arr[0:4]),
        'total_entropy': entropy(count_arr),
        'known_entropy': entropy(count_arr[0:4]),
        'percent_composition': { k:(v / sum(count_arr)) for (k,v) in counts.items() },
        'known_percent_composition': { k:(v / sum(count_arr[0:4])) for (k,v) in known_counts.items() },
    }

def main(): 
    # Perform analysis on all chromosomes
    if MULTIPROCESS_ENABLED:
        with Pool(PROCESS_COUNT) as pool:
            results = pool.map(get_statistics, range(1, 23))
    else:
        results = [ get_statistics(i) for i in range(1, 23) ]

    # Output results
    print(results)
    makedirs(OUTPUT_PATH, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as file:
        file.write(dumps(results, indent=4))

if __name__ == '__main__':
    main()