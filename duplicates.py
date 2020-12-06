import hashlib
import pandas as pd
import os
from os.path import join, getsize

class duplicates:
    # Define hash function
    def hashfile(file, blocksize=65536):

        afile = open(file, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        return hasher.hexdigest()

    def filelist(path):

        full_files = []
        for root, dirs, files in os.walk(path):
            full_files.extend([join(root, x) for x in files])

        return full_files
'''
path = 'C:/Users/carst/Google Drive'
csv_output = 'C:/Users/carst/duplicates.csv'
csv_output2 = 'C:/Users/carst/only_duplicates.csv'

# Calculate checksum of each file
checksum = []
for file in full_files:
    try:
        print(file, end='\r')
        checksum.extend([hashfile(file)])
    except:
        print('Cannot acces file.', end='\r')
        checksum.extend('none')

# Save results to .csv files
df = pd.DataFrame([full_files, checksum]).T
df.columns = ['path', 'hash']
df.set_index('path', inplace=True)

df.to_csv(csv_output)

df.read_csv(csv_output)
#df.dropna(inplace=True)
df = df[df.duplicated(['hash'])]
df.to_csv(csv_output2)
'''
