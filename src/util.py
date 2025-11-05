from os.path import join

DATA_PATH = join('db', 'raw', 'chr%.fa')

def fetch_chromosome(index: int): 
    '''Fetch raw chromosome data by index.'''
    with open(DATA_PATH.replace('%', str(index)), 'r') as file:
        data = ''.join([ line.strip() for line in file.readlines()[1:] ])
    return data