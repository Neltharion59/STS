# Runnable script that creates and persists vector representations for known words using corpora.

import json
import os
import re

from basic_similarity_methods.vector_based_create_vectors import create_vectors_hal
from dataset_modification_scripts.corpora_pool import corpora_pool

# Arg possibilities of vector contruction. Were limited to be computable in reasonable time.
window_size = 10

def store_incidence(center_word, neighbour_word, distance, collecting_parameter):
    value = window_size - distance
    collecting_parameter.append([center_word, neighbour_word, value, collecting_parameter])

def flush_incidence():
    pass

def get_already_processed_line_count(corpus_name):
    pass



pattern = re.compile('[\W_]+')
# For each corpus version - raw vs. lemma
for key in corpora_pool:
    print('----------------------------')
    print(key)
    # For each available corpus
    for corpus in corpora_pool[key]:
        already_processed_line_count = get_already_processed_line_count(corpus.name)
        current_line = 0

        for line in corpus.lines():
            current_line = current_line + 1

            if current_line < already_processed_line_count:
                continue

            words = list(map(lambda word: pattern.sub('', word), line.split[' ']))
            incidences = []

            for i in range(len(words)):
                for j in range(max(0, i-window_size), min(len(words) - 1, i + window_size)):
                    if i == j:
                        continue

                    store_incidence(words[i], words[j], abs(i - j), incidences)
