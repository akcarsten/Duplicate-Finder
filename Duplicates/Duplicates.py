import hashlib
import pandas as pd
import os


class Duplicates:

    def __init__(self):
        self.hash = []

    def __create_table__(self, folder, ext):
        folder = self.__format_path__(folder)
        input_files = self.filelist(folder, ext=ext)

        df = pd.DataFrame(columns=['file', 'hash'])

        df['file'] = input_files
        df['hash'] = self.hashtable(input_files)

        return df

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

    @staticmethod
    def save_csv(csv_path, duplicates):
        csv_file = os.path.join(csv_path, 'duplicates.csv')
        duplicates.to_csv(csv_file, index=False)

    def hashfile(self, file, blocksize=65536):
        with open(file, 'rb') as afile:
            hasher = hashlib.md5()
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
            afile.close()
            self.hash = hasher.hexdigest()

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
        df = self.__create_table__(folder, ext)
        duplicates = df[df['hash'].duplicated(keep=False)]
        duplicates.sort_values(by='hash', inplace=True)

        if to_csv is True:
            self.save_csv(csv_path, duplicates)

        return duplicates

    def find_duplicates(self, file, folder):
        file = self.__format_path__(file)
        folder = self.__format_path__(folder)

        file_hash = self.hashtable(file)

        duplicates = self.list_all_duplicates(folder)

        if len(file_hash) is 1:
            file_hash = file_hash[0]

        return duplicates[duplicates['hash'] == file_hash]

    def compare_folders(self, reference_folder, compare_folder, to_csv=False, csv_path='./', ext=None):

        df_reference = self.__create_table__(reference_folder, ext)
        df_compare = self.__create_table__(compare_folder, ext)

        duplicates = df_reference[df_reference['hash'] == df_compare['hash']]

        if to_csv is True:
            self.save_csv(csv_path, duplicates)

        return duplicates
