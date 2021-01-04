"""Unit tests for the duplicates package"""
import unittest
import os.path
import shutil
import pandas as pd
import duplicates


class TestDetectDuplicates(unittest.TestCase):
    """ Class that holds all test functions"""

    def setUp(self):
        self.output_path = './tmp'
        self.original_file = os.path.join(self.output_path, 'originalFile.csv')
        self.duplicate_file = os.path.join(self.output_path, 'duplicateFile.csv')
        self.expected_hash = 'c137909ea3e82fc45bc17ccef8c691dc'

        os.mkdir(self.output_path)

        test_df = pd.DataFrame(range(0, 5), columns=['test'])
        test_df.to_csv(self.original_file, line_terminator='\r\n')
        # Choosing "\r\n" here because code was written on Windows
        # but should also work on Linux machines with default "\n" line ending

    def tearDown(self):
        shutil.rmtree(self.output_path)

    def copy_folder(self, destination_folder: str):
        """Create a copy of the original folder with its content."""
        os.mkdir(destination_folder)

        destination_folder_file = os.path.join(
            destination_folder, os.path.split(self.duplicate_file)[1])

        shutil.copy(self.original_file, destination_folder_file)

        return destination_folder_file

    def test_hash_method(self):
        """Test the generation of hash identifiers."""
        self.assertEqual(duplicates.hashfile(self.original_file),
                         self.expected_hash)

    def test_fullfile_method_without_subfolders(self):
        """Test the detection of duplicate files without the presence of sub-folders."""
        self.assertEqual(duplicates.filelist(self.output_path)[0],
                         self.original_file)

    def test_fullfile_method_with_subfolders(self):
        """Test the detection of duplicate files when there are files located in sub-folders."""
        sub_folder = os.path.join(self.output_path, 'sub_folder')
        sub_folder_file = self.copy_folder(sub_folder)

        self.assertEqual(duplicates.filelist(self.output_path),
                         [self.original_file, sub_folder_file])

    def test_fullfile_method_with_file_extension(self):
        """Test if the extension parameter works for identifying files of interest."""
        self.assertEqual(duplicates.filelist(self.output_path, ext='.oddExtension'), [])

    def test_hashtable_method(self):
        """Test the generation of hash identifiers from a file list."""
        input_file = duplicates.filelist(self.output_path)

        self.assertEqual(duplicates.hashtable(input_file),
                         [self.expected_hash])

    def test_detection_of_duplicates(self):
        """Test the correct identification of duplicate files."""
        shutil.copy(self.original_file, self.duplicate_file)

        input_files = duplicates.filelist(self.output_path)
        result = duplicates.hashtable(input_files)

        self.assertEqual(result[0], result[1])

    def test_list_all_duplicates_basic_functionality(self):
        """Test the basic functionality of the package
        by validating the correct generation of the data frame."""
        shutil.copy(self.original_file, self.duplicate_file)

        result = duplicates.list_all_duplicates(self.output_path)

        self.assertEqual(list(result.columns), ['file', 'hash'])

        self.assertEqual(result['hash'].unique()[0],
                         self.expected_hash)

        self.assertEqual(result['hash'].shape[0], 2)

    def test_list_all_duplicates_save_csv(self):
        """Test the export of the results to a .csv file."""
        shutil.copy(self.original_file, self.duplicate_file)

        duplicates.list_all_duplicates(
            self.output_path, to_csv=True, csv_path=self.output_path)

        expected = os.path.join(self.output_path, 'duplicateFile.csv')
        self.assertTrue(os.path.isfile(expected))

    def test_find_duplicates_basic_functionality(self):
        """Test if a specific file can be used as a reference to find its duplicate."""
        shutil.copy(self.original_file, self.duplicate_file)

        file = duplicates.filelist(self.output_path)[0]

        result = duplicates.find_duplicates(file, self.output_path)

        self.assertEqual(result['hash'].unique()[0],
                         self.expected_hash)

        self.assertEqual(sorted(list(result['file'])),
                         [os.path.abspath('tmp{}duplicateFile.csv'.format(os.path.sep)),
                          os.path.abspath('tmp{}originalFile.csv'.format(os.path.sep))])
        # sorting the list here to make the test run on Windows and Linux

    def test_compare_folders_basic_functionality(self):
        """Test the comparison of two folders against each other."""
        reference_folder = os.path.join(self.output_path, 'reference_folder')
        compare_folder = os.path.join(self.output_path, 'compare_folder')

        self.copy_folder(compare_folder)
        reference_folder_file = self.copy_folder(reference_folder)

        duplicate_files = duplicates.compare_folders(reference_folder, reference_folder)

        self.assertEqual(duplicate_files['file'].values[0], os.path.abspath(reference_folder_file))
