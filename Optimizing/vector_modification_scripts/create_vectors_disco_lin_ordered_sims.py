import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import datetime
from json import dumps, loads

from util.file_handling import read, write
from corpora_modification_scripts.Util import get_unique_dataset_words, get_non_stop_feature_words

vector_file_path_lin = './resources/vector/disco_lin.json'
vector_file_path_lin_sims = './resources/vector/disco_lin_sims.json'

vector_words = get_unique_dataset_words()
feature_words = get_non_stop_feature_words()
window_radius = 5

print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Reading lin vectors.')
vectors_lin = loads(read(vector_file_path_lin))
print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Lin vectors read.')

try:
    vectors_lin_sims = loads(read(vector_file_path_lin_sims))
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Loaded existing sim vectors.')
except FileNotFoundError:
    vectors_lin_sims = {}
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Creating new sim vectors.')

for vector_word1 in vector_words:
    if vector_word1 in vectors_lin_sims:
        continue

    sims = []
    for vector_word2 in vector_words:

        sum_top = 0
        sum_bottom = 0

        for feature_word in feature_words:
            for p in range(window_radius):
                increment = vectors_lin[vector_word1][feature_word][p] + vectors_lin[vector_word2][feature_word][p]

                if vectors_lin[vector_word1][feature_word][p] > 0 and vectors_lin[vector_word2][feature_word][p] > 0:
                    sum_top = sum_top + increment

                sum_bottom = sum_bottom + increment

        similarity = abs(round(sum_top/sum_bottom, 4))
        sims.append({'word': vector_word2, 'sim': similarity})

    sims = sorted(sims, key=lambda element: element['sim'], reverse=True)
    print(sims)
    exit(1)
    vectors_lin_sims[vector_word1] = sims
    write(vector_file_path_lin_sims, dumps(vectors_lin_sims))


