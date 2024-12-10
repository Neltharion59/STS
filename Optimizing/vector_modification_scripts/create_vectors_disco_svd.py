import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import datetime
from json import dumps

from util.math import svd_part_1, svd_part_2
from util.file_handling import read, write
from corpora_modification_scripts.Util import get_non_stop_feature_words, get_stop_words

vector_file_path_raw = '../resources/vector/disco_raw.txt'
vector_file_path_svd_pattern = '../resources/vector/disco_svd_{0}.json'

vector_sizes = [100, 200, 300, 400, 500, 600, 700, 800]

feature_words = filter(lambda word: word not in get_stop_words(), get_non_stop_feature_words())

vectors_raw = read(vector_file_path_raw)

matrix_raw = [sum([vectors_raw[vector_word][feature_word] for feature_word in feature_words]) for vector_word in vectors_raw]
svd_matrix_part_1 = None

for vector_size in vector_sizes:
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Running vector size: "{vector_size}".')

    vector_file_path_svd = vector_file_path_svd_pattern.format(vector_size)

    if os.path.exists(vector_file_path_svd):
        print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Already exists')
        continue

    if svd_matrix_part_1 is None:
        print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Calculating part 1')
        svd_matrix_part_1 = svd_part_1(matrix_raw)
        print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Calculated part 1')
    else:
        print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Part 1 Already calculated')

    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Calculating part 2')
    matrix_svd = svd_part_2(svd_matrix_part_1, vector_size)
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Calculated part 2')

    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Transforming to vectors')
    vectors_svd = {word: row for word, row in zip(list(vectors_raw.keys()), matrix_svd)}

    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Dumping to json')
    vectors_svd_json = dumps(vectors_svd)

    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Writing to file')
    write(vector_file_path_svd, vectors_svd_json)

print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Over')