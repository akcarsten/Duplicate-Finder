import hashlib
import os


class Duplicates:

    def __init__(self):
        self.hash = []

    @staticmethod
    def filelist(filepath):

        file_list = []
        for path, subdirs, files in os.walk(filepath):
            for name in files:
                file_list.append(os.path.join(path, name))

        return file_list

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

        hash_identifier = []
        for file in files:
            print(file, end='\r')
            hash_identifier.extend([self.hashfile(file)])

        return hash_identifier
