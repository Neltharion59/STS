import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps
from util.file_handling import read, write
from util.math import short_svd

vector_file_path_svd_pattern = './resources/vector/hal_svd_{0}.json'

vectors_hal_full = [[line.split('\t')[0], line.split('\t')[1].split(',')] for line in read('./resources/vector/hal_full.txt').split('\n') if len(line) > 0]
matrix_hal_full = [record[1] for record in vectors_hal_full]

vector_sizes = [100, 200, 300, 400, 500, 600, 700, 800]

for vector_size in vector_sizes:
    vector_file_path_svd = vector_file_path_svd_pattern.format(vector_size)

    matrix_svd = short_svd(matrix_hal_full, vector_size)
    vectors_svd = {word: row for word, row in zip([record[0] for record in vectors_hal_full], matrix_svd)}
    vectors_svd_json = dumps(vectors_svd)
    write(vector_file_path_svd, vectors_svd_json)
