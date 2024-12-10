import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import datetime
from json import dumps, loads
from math import log10

from util.file_handling import read, write
from corpora_modification_scripts.Util import get_unique_dataset_words, get_non_stop_feature_words, get_stop_words

vector_file_path_raw = './resources/vector/disco_raw.txt'
vector_file_path_lin = './resources/vector/disco_lin.json'

vector_words = get_unique_dataset_words()
feature_words = filter(lambda word: word not in get_stop_words(), get_non_stop_feature_words())

vectors_raw = read(vector_file_path_raw)

distances = [1, 2, 3, 4, 5]
feature_words_merged = {distance: {f_word: sum(vectors_raw[v_word][f_word][distance - 1] for v_word in vector_words) for f_word in feature_words} for distance in distances}
print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Prepared FEATURE distances for fast calc.')
distances_merged = {distance: sum([feature_words_merged[distance][f_word] for f_word in feature_words_merged[distance]]) for distance in distances}
print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Prepared DISTANCE distances for fast calc.')
vector_words_merged = {distance: {v_word: sum(vectors_raw[v_word][f_word][distance - 1] for f_word in feature_words) for v_word in vector_words} for distance in distances}
print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Prepared VECTOR distances for fast calc.')

print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Prepared ALL distances for fast calc.')


def calc_value(vector_word, feature_word, distance):
    return log10(((vectors_raw[vector_word][feature_word][distance - 1] - 0.95) * distances_merged[distance])/(vector_words_merged[distance][vector_word]*feature_words_merged[distance][feature_word]))


try:
    vectors_lin = loads(read(vector_file_path_lin))
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Loaded existing vectors.')
except FileNotFoundError:
    vectors_lin = {}
    print(f'[{datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}] Creating new vectors.')

for vector_word in vector_words:
    if vector_word not in vectors_lin:
        vectors_lin[vector_word] = {}

    added = False
    for feature_word in feature_words:
        if feature_word in vectors_lin[vector_word]:
            continue

        print(f'Calcing for vw:"{vector_word}", fw:"{feature_word}".')
        added = True
        vectors_lin[vector_word][feature_word] = [calc_value(vector_word, feature_word, distance) for distance in distances]
        print(f'Calced".')

    if added:
        print(f'Dumping".')
        write(vector_file_path_lin, dumps(vectors_lin))
        print(f'Dumped".')
