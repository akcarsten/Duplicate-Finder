import unittest
import pandas as pd
import os.path
import shutil
from create_parquet_dataset import *


class TestDetectDuplicates(unittest.TestCase):

        def setUp(self):
            self.output_path = 'tmp'
            self.output_file = 'duplicates.csv'

            os.mkdir(self.output_path)


        def tearDown(self):
            shutil.rmtree(self.output_path)

        def test_if_parquet_file_is_created(self):

                create_parquet_dataset(self.input_file, self.output_file)
                self.assertTrue(os.path.isfile(self.output_file))
