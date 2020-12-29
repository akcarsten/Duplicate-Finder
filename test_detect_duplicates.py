import unittest
import pandas as pd
import os.path
import shutil
from Duplicates import Duplicates


class TestDetectDuplicates(unittest.TestCase):

    def setUp(self):
        self.output_path = 'tmp'
        self.output_file = '{}/duplicates.csv'.format(self.output_path)
        self.test_file = '{}/testFile.csv'.format(self.output_path)
        self.expected_hash = 'c137909ea3e82fc45bc17ccef8c691dc'

        self.duplicates = Duplicates()

        os.mkdir(self.output_path)

        df = pd.DataFrame(range(0, 5), columns=['test'])
        df.to_csv(self.test_file)

    def tearDown(self):
        shutil.rmtree(self.output_path)

    def test_hash_method(self):

        self.assertEqual(self.duplicates.hashfile(self.test_file),
                         self.expected_hash)

    def test_fullfile_without_subfolders(self):

        self.assertEqual(self.duplicates.filelist(self.output_path),
                         ['tmp\\testFile.csv'])

    def test_fullfile_with_subfolders(self):

        print('test')

    def test_hashtable_method(self):

        input_file = self.duplicates.filelist(self.output_path)
        self.assertEqual(self.duplicates.hashtable(input_file),
                         [self.expected_hash])

    def test_detection_of_duplicates(self):

        start_file = self.duplicates.filelist(self.output_path)
        name = start_file[0].split('.csv')
        duplicate_file = '{}_duplicate.csv'.format(name[0])

        shutil.copy(start_file[0], duplicate_file)

        input_files = self.duplicates.filelist(self.output_path)
        result = self.duplicates.hashtable(input_files)

        self.assertEqual(result[0], result[1])
