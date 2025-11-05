'''
Fetches data from ucsc.edu and preps it for use. Stores data in data/ directory
'''
from requests import get
from os.path import join, exists
from shutil import rmtree
from os import makedirs
from io import BytesIO
import gzip

BASE_URL='https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr%.fa.gz'

DB_PATH = 'db'
RAW_DATA_PATH = join(DB_PATH, 'raw')

#
# DOWNLOADING DATA
#

DOWNLOAD_URLS = [ BASE_URL.replace('%', str(i)) for i in range(1, 23)]

if exists(RAW_DATA_PATH):
    usrOpt = input('Raw data already exists. Download anyways? (Y/n): ')
    if usrOpt != 'Y':
        print('Skipping download and exiting.')
        exit(0)
    else:
        rmtree(RAW_DATA_PATH)
        makedirs(RAW_DATA_PATH)


for i in range(len(DOWNLOAD_URLS)):
    url = DOWNLOAD_URLS[i]
    file_name = f'chr{i + 1}.fa'

    print(f'Downloading: {url}')
    request = get(url)
    print(f'Unzipping: {file_name}.gz')
    with gzip.GzipFile(fileobj=BytesIO(request.content), mode='rb') as raw_data:
        with open(join(RAW_DATA_PATH, file_name), 'wb') as out_file:
            out_file.write(raw_data.read())
    print(f'Download complete: {file_name}')