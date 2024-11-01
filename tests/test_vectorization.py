import unittest
from src.vectorization import generate_embeddings

class TestVectorization(unittest.TestCase):
    def test_generate_embeddings(self):
        """
        Test the generate_embeddings function.
        """

        texts = ["This is a test.", "Another test."]
        results = generate_embeddings(texts)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].shape, (768,))
        self.assertEqual(results[1].shape, (768,))

if __name__ == '__main__':
    unittest.main()
