import hashlib
import pandas as pd
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

        try:
            afile = open(file, 'rb')
            hasher = hashlib.md5()
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
            afile.close()
            self.hash = hasher.hexdigest()

        except OSError:
            self.hash = 'File does not exist'

        return self.hash

    def hashtable(self, files):

        hash_identifier = []
        for file in files:
            print(file, end='\r')
            hash_identifier.extend([self.hashfile(file)])

        return hash_identifier

    def list_all_duplicates(self, folder, to_csv=False, csv_path='./'):
        input_files = self.filelist(folder)

        df = pd.DataFrame(columns=['file', 'hash'])

        df['file'] = input_files
        df['hash'] = self.hashtable(input_files)

        duplicates = df[df['hash'].duplicated(keep=False)]
        duplicates.sort_values(by='hash', inplace=True)

        if to_csv is True:
            csv_file = os.path.join(csv_path, 'duplicates.csv')
            duplicates.to_csv(csv_file, index=False)

        return duplicates

    def find_duplicates(self, file, folder):
        file_path = [file.replace('/', os.path.sep)]

        file_hash = self.hashtable(file_path)[0]

        duplicates = self.list_all_duplicates(folder)

        return duplicates[duplicates['hash'] == file_hash]
