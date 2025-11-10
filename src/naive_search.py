'''
Searches chromosomes for a particular motif using a naive searching algorithm.
'''
from util import fetch_chromosome
from multiprocessing import Pool
from os.path import join
from json import dumps

# CONFIGURATION
PROCESS_COUNT = 22
MOTIF = 'ACTACGA'

OUTPUT_PATH = 'out'
OUTPUT_FILE = join(OUTPUT_PATH, 'search_results.json')

def search_sequence(sequence: str, motif: str):
    '''Searches a sequence for a particular motif, returning all indexes
    where the motif is found.'''
    occurrences = []
    for i in range(0, len(sequence) - len(motif) + 1):
        j = 0
        while j < len(motif) and sequence[i + j] == motif[j]:
            j += 1 
        if j == len(motif):
            occurrences.append(i)
            i += j
    return occurrences

def search_task(chrIndex: int):
    '''Accepts a chromosome index and returns all indicies where the
    motif is found.'''
    print(f'[BEGIN] {chrIndex}.')
    chromosome = fetch_chromosome(chrIndex)
    results = search_sequence(chromosome, MOTIF)
    print(f'[COMPLETE] chr{chrIndex}.')
    return results

def main():
    # search all chromosomes
    with Pool(PROCESS_COUNT) as pool:
        results = pool.map(search_task, range(1,23))
    
    # map to dict
    out = {
        'motif': MOTIF,
        'results': {},
    }
    for i in range(len(results)):
        out['results'][f'chr{i + 1}'] = {
            'total_occurrences': len(results[i]),
            'occurrences': results[i]
        }

    # write data to file
    with open(OUTPUT_FILE, 'w') as file:
        file.write(dumps(out, indent=4))

if __name__ == '__main__':
    main()