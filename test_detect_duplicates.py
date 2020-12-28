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

            df = pd.DataFrame(range(0,5), columns=['test'])
            df.to_csv(self.test_file)

        def tearDown(self):
            shutil.rmtree(self.output_path)

        def test_hash_function(self):

                self.assertEqual(self.duplicates.hashfile(self.test_file),
                                 self.expected_hash)

        def test_fullfile_function(self):

            self.assertEqual(self.duplicates.filelist(self.output_path),
                             ['tmp\\testFile.csv'])

        def test_hashtable_function(self):

            inputfile = self.duplicates.filelist(self.output_path)
            self.assertEqual(self.duplicates.hashtable(inputfile),
                             [self.expected_hash])

        def test_detect_dupliacte(self):

            start_file = self.duplicates.filelist(self.output_path)
            name = start_file[0].split('.csv')
            duplicatefile = '{}_duplicate.csv'.format(name[0])

            shutil.copy(start_file[0], duplicatefile)

            inputfiles = self.duplicates.filelist(self.output_path)
            result = self.duplicates.hashtable(inputfiles)

            self.assertEqual(result[0], result[1])
