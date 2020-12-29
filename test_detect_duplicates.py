import unittest
import pandas as pd
import os.path
import shutil
from Duplicates import Duplicates


class TestDetectDuplicates(unittest.TestCase):

    def setUp(self):
        self.output_path = 'tmp'
        self.original_file = os.path.join(self.output_path, 'originalFile.csv')
        self.duplicate_file = os.path.join(self.output_path, 'duplicateFile.csv')
        self.expected_hash = 'c137909ea3e82fc45bc17ccef8c691dc'

        self.duplicates = Duplicates()

        os.mkdir(self.output_path)

        df = pd.DataFrame(range(0, 5), columns=['test'])
        df.to_csv(self.original_file)

    def tearDown(self):
        shutil.rmtree(self.output_path)

    def test_hash_method(self):
        self.assertEqual(self.duplicates.hashfile(self.original_file),
                         self.expected_hash)

    def test_fullfile_without_subfolders(self):
        self.assertEqual(self.duplicates.filelist(self.output_path)[0],
                         self.original_file)

    def test_fullfile_with_invalid_characters(self):
        invalid_file = r'\?\{}\{}.csv'.format(os.path.abspath(self.output_path), 'tooLong' * 40)

        os.makedirs(invalid_file)

        input_file = self.duplicates.filelist(self.output_path)

        self.duplicates.hashtable(input_file)

    def test_fullfile_with_subfolders(self):
        sub_folder = os.path.join(self.output_path, 'sub_folder')
        os.mkdir(sub_folder)

        sub_folder_file = os.path.join(sub_folder, os.path.split(self.duplicate_file)[1])

        shutil.copy(self.original_file, sub_folder_file)

        self.assertEqual(self.duplicates.filelist(self.output_path),
                         [self.original_file, sub_folder_file])

    def test_hashtable_method(self):
        input_file = self.duplicates.filelist(self.output_path)
        self.assertEqual(self.duplicates.hashtable(input_file),
                         [self.expected_hash])

    def test_detection_of_duplicates(self):
        shutil.copy(self.original_file, self.duplicate_file)

        input_files = self.duplicates.filelist(self.output_path)
        result = self.duplicates.hashtable(input_files)

        self.assertEqual(result[0], result[1])
