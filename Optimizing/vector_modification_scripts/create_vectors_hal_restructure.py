import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps
from util.file_handling import read, write
from util.math import short_svd

vector_file_path_output = './resources/vector/hal_full.json'

vectors_hal_full = {line.split('\t')[0]: line.split('\t')[1].split(',') for line in read('./resources/vector/hal_full.txt').split('\n') if len(line) > 0}
for key in vectors_hal_full:
    vectors_hal_full[key] = [float(x) for x in vectors_hal_full[key]]

write(vector_file_path_output, dumps(vectors_hal_full))
