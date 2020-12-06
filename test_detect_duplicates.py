import unittest
import pandas as pd
import os.path
import shutil
from duplicates import *


class TestDetectDuplicates(unittest.TestCase):

        def setUp(self):
            self.output_path = 'tmp'
            self.output_file = '{}/duplicates.csv'.format(self.output_path)
            self.test_file = '{}/testFile.csv'.format(self.output_path)

            os.mkdir(self.output_path)

            df = pd.DataFrame(range(0,5), columns=['test'])
            df.to_csv(self.test_file)

        def tearDown(self):
            shutil.rmtree(self.output_path)

        def test_hash_function(self):

                self.assertEqual(duplicates.hashfile(self.test_file),
                                 'c137909ea3e82fc45bc17ccef8c691dc')
