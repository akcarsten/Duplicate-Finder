import hashlib
import pandas as pd
import os
from os.path import join, getsize

class Duplicates:

    def __init__(self):
        pass

    def hashfile(self, file, blocksize=65536):

        afile = open(file, 'rb')
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        afile.close()
        self.hash = hasher.hexdigest()

        return self.hash

    @staticmethod
    def filelist(filepath):

        files = ['{}\\{}'.format(filepath, x) for x in os.listdir(filepath)]
        return files

    def hashtable(files):
        print(files)
        hash = []
        for file in files:
                print(file, end='\r')
                hash.extend([self.hashfile(file)])

        return hash

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
