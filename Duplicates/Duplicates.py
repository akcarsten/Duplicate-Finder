import hashlib
import pandas as pd
import os


class Duplicates:
    """ Duplicate class that holds all methods for finding duplicate files."""

    def __init__(self):
        self.hash = []

    def __create_table(self, folder: str, ext: str) -> pd.DataFrame:
        """Create a Pandas dataframe with a column 'file' for the path to a file and a
        column 'hash' with the corresponding hash identifier."""

        folder = self.__format_path(folder)
        input_files = self.filelist(folder, ext=ext)

        df = pd.DataFrame(columns=['file', 'hash'])

        df['file'] = input_files
        df['hash'] = self.hashtable(input_files)

        return df

    @staticmethod
    def __format_path(file: str) -> str:
        """Format a path according to the systems separator."""

        return os.path.abspath([file.replace('/', os.path.sep)][0])

    @staticmethod
    def filelist(filepath: str, ext: str = None) -> list:
        """ Lists all files in a folder including sub-folders.
        If only files with a specific extension are of interest this can be specified by the 'ext' parameter."""

        file_list = []
        for path, subdirs, files in os.walk(filepath):
            for name in files:
                _, extension = os.path.splitext(name)
                if ext is None or extension == ext:
                    file_list.append(os.path.join(path, name))

        return file_list

    @staticmethod
    def save_csv(csv_path: str, duplicates: pd.DataFrame) -> None:
        """Save a Pandas dataframe as a csv file."""

        csv_file = os.path.join(csv_path, 'duplicates.csv')
        duplicates.to_csv(csv_file, index=False)

    def hashfile(self, file: str, blocksize: int = 65536) -> str:
        """Generate the hash of any file according to the md5 algorithm."""

        with open(file, 'rb') as afile:
            hasher = hashlib.md5()
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
            afile.close()
            self.hash = hasher.hexdigest()

        return self.hash

    def hashtable(self, files: str) -> list:
        """Go through a list of files and calculate their hash identifiers."""

        if type(files) is not list:
            files = [files]

        hash_identifier = []
        for file in files:
            print(file, end='\r')
            hash_identifier.extend([self.hashfile(file)])

        return hash_identifier

    def list_all_duplicates(self, folder: str,
                            to_csv: bool = False, csv_path: str = './', ext: str = None) -> pd.DataFrame:
        """Go through a folder and find all duplicate files.
        The returned dataframe contains all files, not only the duplicates.
        With the 'to_csv' parameter the results can also be saved in a .csv file.
        The location of that .csv file can be specified by the 'csv_path' parameter."""

        df = self.__create_table(folder, ext)
        duplicates = df[df['hash'].duplicated(keep=False)]
        duplicates.sort_values(by='hash', inplace=True)

        if to_csv is True:
            self.save_csv(csv_path, duplicates)

        return duplicates

    def find_duplicates(self, file: str, folder: str) -> pd.DataFrame:
        """Search a folder for duplicates of a file of interest. In contrast to 'list_all_duplicates', this allows
        limiting the search to one particular file."""

        file = self.__format_path(file)
        folder = self.__format_path(folder)

        file_hash = self.hashtable(file)

        duplicates = self.list_all_duplicates(folder)

        if len(file_hash) == 1:
            file_hash = file_hash[0]

        return duplicates[duplicates['hash'] == file_hash]

    def compare_folders(self, reference_folder: str, compare_folder: str,
                        to_csv: bool = False, csv_path: str = './', ext: str = None) -> pd.DataFrame:
        """Directly compare two folders of interest and identify duplicates between them.
        With the 'to_csv' parameter the results can also be saved in a .csv file.
        The location of that .csv file can be specified by the 'csv_path' parameter.
        Further the search can be limited to files with a specific extension via the 'ext' parameter."""

        df_reference = self.__create_table(reference_folder, ext)
        df_compare = self.__create_table(compare_folder, ext)

        duplicates = df_reference[df_reference['hash'] == df_compare['hash']]

        if to_csv is True:
            self.save_csv(csv_path, duplicates)

        return duplicates
