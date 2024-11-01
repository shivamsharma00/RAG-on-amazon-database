# tests/test_preprocessing.py

import unittest
from src.preprocessing import preprocess_text

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_text(self):
        input_text = "<p>This is a test</p>"
        expected_output = "this is a test"
        self.assertEqual(preprocess_text(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
