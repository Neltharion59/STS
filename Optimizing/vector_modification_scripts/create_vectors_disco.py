import sys
import os
conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from os import listdir, fsync
from os.path import isfile, join
from functools import reduce
import re
import mysql.connector
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words, get_non_stop_feature_words

window_radius = 5
frame_size = window_radius * 2 + 1

vector_words = get_unique_dataset_words()
feature_words = get_non_stop_feature_words()


def is_vector_word(word):
    return word in vector_words


def is_feature_word(word):
    return word in feature_words


vector_file_path = '../resources/vector/disco_raw.txt'


def save_vectors(vectors):
    new_lines = []
    for vector_word in vector_words:
        new_line = vector_word + '\t' + ','.join([str(x) for x in reduce(lambda a,b: a+b, [vectors[vector_word][feature_word] for feature_word in feature_words])]) + '\n'
        new_lines.append(new_line)

    with open(vector_file_path, 'w+', encoding='utf-8') as vector_file:
        vector_file.writelines(new_lines)
        vector_file.flush()
        fsync(vector_file)


def chunk_array(array, chunk_size):
    if len(array) % chunk_size != 0:
        raise Exception

    for i in range(len(array)//chunk_size):
        yield array[chunk_size * i: chunk_size * (i+1)]

def init_vectors():
    try:
        with open(vector_file_path, 'r', encoding='utf-8') as vector_file:
            lines = vector_file.readlines()
    except FileNotFoundError:
        return {vector_word: {feature_word: [0] * window_radius for feature_word in feature_words} for vector_word in vector_words}

    initialized_vectors = {}
    for line in lines:
        tokens = line.split('\t')
        vector_word = tokens[0]
        vector = {feature_word:values for feature_word, values in zip(feature_words, chunk_array([int(x) for x in tokens[1].split(',')], window_radius))}
        initialized_vectors[vector_word] = vector

    return initialized_vectors


def get_corpus_file_id(corpus_file_name):
    return corpus_file_name.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')


corpora_directory_path = './../resources/corpora/processed/'

corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = sorted([x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)], key=lambda x: int(get_corpus_file_id(x)))
corpus_progress_track_file_name_pattern = "progress_vector_disco_construction_oscarsk_{}"

vectors = init_vectors()

for input_corpus_file in input_corpus_files:
    corpus_file_path = join(corpora_directory_path, input_corpus_file)
    dataset_part_id = corpus_file_path.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')
    progress_file_path = './../resources/temp/' + corpus_progress_track_file_name_pattern.format(dataset_part_id) + '.txt'

    last_processed_line = 0
    try:
        with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
            last_processed_line = int(progress_file.read())
    except FileNotFoundError:
        pass

    if last_processed_line == -1:
        continue

    current_line = 0
    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        total_lines = len(corpus_file.readlines())

    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        for line in corpus_file:
            current_line = current_line + 1

            print(f'{input_corpus_file} Processing line {str(current_line)}/{str(total_lines)} - {str(current_line/total_lines*100)}%')

            tokens = split_to_words(line)
            for i in range(len(tokens)):
                if not is_vector_word(tokens[i]):
                    continue

                for j in range(max(0, i - window_radius), min(len(tokens), i + window_radius)):
                    if i == j:
                        continue

                    if not is_feature_word(tokens[j]):
                        continue

                    distance = abs(i - j)
                    array_index = distance - 1
                    vectors[tokens[i]][tokens[j]][array_index] = vectors[tokens[i]][tokens[j]][array_index] + 1

        print('---saving---')
        save_vectors(vectors)
        with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
            progress_file.write(str(-1))
            progress_file.flush()
            fsync(progress_file)
