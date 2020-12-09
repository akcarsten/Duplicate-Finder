import hashlib
import pandas as pd
import os
from os.path import join, getsize

class Duplicates:

    def __init__(self):
        self.hash = []

    @staticmethod
    def filelist(filepath):

        files = ['{}\\{}'.format(filepath, x) for x in os.listdir(filepath)]
        return files

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

    def hashtable(self, files):

        hash = []
        for file in files:
                print(file, end='\r')
                hash.extend([self.hashfile(file)])

        return hash
