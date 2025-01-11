import unittest

import os
from unittest import TestCase

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from basic_similarity_methods.vector_based import vectorize_text
from dataset_modification_scripts.lemmatize.lemmatizer_wrapper import Lemmatizer

lemmatizer = Lemmatizer(root_path)


class tests_vectorize(TestCase):

    def test___pad___skip___add(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [3, 4, 1, 0]
        expected_vec2 = [1, 1, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___skip___add_pos_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add_pos_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [6, 8, 1, 0]
        expected_vec2 = [2, 2, 2, 2]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___skip___add_power11_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add_power11_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [33, 44, 1, 0]
        expected_vec2 = [11, 11, 11, 11]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___skip___concat_pad(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'concat_pad'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 1, 0, 3, 4, 0, 0]
        expected_vec2 = [1, 1, 1, 1, 0, 0, 0, 0]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___skip___concat_cutoff(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'concat_cutoff'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 1, 0]
        expected_vec2 = [1, 1, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___zeroes___add(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [3, 4, 1, 0]
        expected_vec2 = [1, 1, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___zeroes___add_pos_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add_pos_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [6, 8, 1, 0]
        expected_vec2 = [2, 2, 2, 2]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___zeroes___add_power11_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add_power11_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [33, 44, 1, 0]
        expected_vec2 = [11, 11, 11, 11]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___zeroes___concat_pad(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'concat_pad'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 1, 0, 3, 4, 0, 0]
        expected_vec2 = [0, 0, 0, 0, 1, 1, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___pad___zeroes___concat_cutoff(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'pad',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'concat_cutoff'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 1, 0, 3, 4, 0, 0]
        expected_vec2 = [0, 0, 0, 0, 1, 1, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___skip___add(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [3, 4]
        expected_vec2 = [1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___skip___add_pos_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add_pos_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [6, 8]
        expected_vec2 = [2, 2]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___skip___add_power11_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'add_power11_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [33, 44]
        expected_vec2 = [11, 11]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___skip___concat_pad(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'concat_pad'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 3, 4]
        expected_vec2 = [1, 1, 0, 0]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___skip___concat_cutoff(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'skip',
            'vector_merge_strategy': 'concat_cutoff'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0]
        expected_vec2 = [1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___zeroes___add(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [3, 4]
        expected_vec2 = [1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___zeroes___add_pos_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add_pos_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [6, 8]
        expected_vec2 = [2, 2]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___zeroes___add_power11_weight(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'add_power11_weight'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [33, 44]
        expected_vec2 = [11, 11]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___zeroes___concat_pad(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'concat_pad'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 3, 4]
        expected_vec2 = [0, 0, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)

    def test___cutoff___zeroes___concat_cutoff(self):
        text1 = "pes strom"
        text2 = "hrob hrad"

        cache = {
            'lemmatizer': lemmatizer,
            'vectors': {
                'pes': [0, 0, 1],
                'strom': [3, 4],
                'hrad': [1, 1, 1, 1]
            }
        }

        args = {
            'normalize_word_vector_length_strategy': 'cutoff',
            'missing_vector_strategy': 'zeroes',
            'vector_merge_strategy': 'concat_cutoff'
        }

        vec1, vec2 = vectorize_text(text1, text2, args, cache)

        expected_vec1 = [0, 0, 3, 4]
        expected_vec2 = [0, 0, 1, 1]

        self.assertListEqual(expected_vec1, vec1)
        self.assertListEqual(expected_vec2, vec2)


if __name__ == '__main__':
    unittest.main()
