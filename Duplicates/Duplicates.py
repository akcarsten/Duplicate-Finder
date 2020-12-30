import hashlib
import pandas as pd
import os


class Duplicates:

    def __init__(self):
        self.hash = []

    @staticmethod
    def __format_path__(file):
        return os.path.abspath([file.replace('/', os.path.sep)][0])

    @staticmethod
    def filelist(filepath, ext=None):

        file_list = []
        for path, subdirs, files in os.walk(filepath):
            for name in files:
                _, extension = os.path.splitext(name)
                if ext is None or extension == ext:
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
        if type(files) is not list:
            files = [files]

        hash_identifier = []
        for file in files:
            print(file, end='\r')
            hash_identifier.extend([self.hashfile(file)])

        return hash_identifier

    def list_all_duplicates(self, folder, to_csv=False, csv_path='./', ext=None):
        folder = self.__format_path__(folder)
        input_files = self.filelist(folder, ext=ext)

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
        file = self.__format_path__(file)
        folder = self.__format_path__(folder)

        file_hash = self.hashtable(file)

        duplicates = self.list_all_duplicates(folder)

        if len(file_hash) is 1:
            file_hash = file_hash[0]

        return duplicates[duplicates['hash'] == file_hash]

    def compare_folders(self, reference_folder, compare_folder):
        reference_folder = self.__format_path__(reference_folder)
        compare_folder = self.__format_path__(compare_folder)
