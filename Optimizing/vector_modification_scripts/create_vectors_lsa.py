import gc
import json
import math
import sys
import os
conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from os import listdir, fsync
from os.path import isfile, join
from functools import reduce
import re
import mysql.connector
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words

corpora_directory_path = './../resources/corpora/processed/'
vector_words = [word for word in get_unique_dataset_words()]


def get_corpus_file_id(corpus_file_name):
    return corpus_file_name.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')


def chunk_array(array, chunk_size):
    for i in range(math.ceil(len(array)/chunk_size)):
        start_index =chunk_size * i
        end_index = min(chunk_size * (i+1), len(array))
        yield array[start_index: end_index]


chunk_size = 1000
vector_word_batches = list(chunk_array(vector_words, chunk_size))
batch_count = len(vector_word_batches)
vector_file_path = '../resources/vector/lsa_full_{}_{}.txt'


def save_vectors(vectors, batch_id, chunk_size):
    new_lines = []
    line_n = 0
    for vector_word in vectors:
        line_n = line_n + 1
        print(f'Saving line {line_n}/{chunk_size}')
        new_line = vector_word + '\t' + ','.join(
            [str(value) for value in vectors[vector_word]]) + '\n'
        new_lines.append(new_line)

    print('Persisting vectors')
    path = vector_file_path.format(batch_id, chunk_size)
    with open(path, 'w+', encoding='utf-8') as vector_file:
        vector_file.writelines(new_lines)
        vector_file.flush()
        fsync(vector_file)
    print('Persisted vectors')


corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = sorted([x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)], key=lambda x: int(get_corpus_file_id(x)))
corpus_progress_track_file_name_pattern = "progress_vector_lsa_construction_oscarsk_{}"
line_counts_file_path = '../resources/corpora_line_counts.txt'

line_counts = []
print('Getting line counts')
try:
    with open(line_counts_file_path, 'r', encoding='utf-8') as line_counts_file:
        line_counts = json.loads(line_counts_file.read())
except FileNotFoundError:

    for input_corpus_file in input_corpus_files:
        print(input_corpus_file)
        corpus_file_path = join(corpora_directory_path, input_corpus_file)
        with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
            line_counts.append(len(corpus_file.readlines()))

    with open(line_counts_file_path, 'w+', encoding='utf-8') as line_counts_file:
        line_counts_file.write(json.dumps(line_counts))
print('Finished getting line counts')
total_lines = sum(line_counts)
print(total_lines)


def init_vectors(batch_id, chunk_size):
    path = vector_file_path.format(batch_id, chunk_size)
    try:
        with open(path, 'r', encoding='utf-8') as vector_file:
            lines = vector_file.readlines()
    except FileNotFoundError:
        return {word: [0]*total_lines for word in vector_word_batches[batch_id]}

    initialized_vectors = {}
    line_ctn = 0
    for line in lines:
        line_ctn = line_ctn + 1
        tokens = line.split('\t')
        vector_word = tokens[0]
        print(f'Loading pre-existing vector {line_ctn}/{chunk_size}: "{vector_word}"')
        vector = [int(value) for value in tokens[1].split(',')]
        initialized_vectors[vector_word] = vector

    return initialized_vectors


print('Initialiting vectors')
print('Vectors initialized')


for batch_id in range(len(vector_word_batches)):
    batch_order = batch_id + 1
    current_line = 0
    current_batch = vector_word_batches[batch_id]

    vectors = {}
    gc.collect()
    for i in range(len(input_corpus_files)):
        input_corpus_file = input_corpus_files[i]
        corpus_file_path = join(corpora_directory_path, input_corpus_file)
        dataset_part_id = get_corpus_file_id(corpus_file_path)
        progress_file_path = f'./../resources/temp/{corpus_progress_track_file_name_pattern.format(dataset_part_id)}_ch_{batch_id}_{chunk_size}.txt'

        last_processed_line = 0
        try:
            with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
                last_processed_line = int(progress_file.read())
                print(f'Progress file {progress_file_path} found')
        except FileNotFoundError:
            print(f'Progress file {progress_file_path} not found')
            pass

        if last_processed_line == -1:
            current_line = current_line + line_counts[i]
            continue

        if len(list(vectors.keys())) == 0:
            vectors = init_vectors(batch_id, chunk_size)

        with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
            for line in corpus_file:

                print(f'Batch {batch_order}/{batch_count}. {input_corpus_file}. Processing line {str(current_line)}/{str(total_lines)} - {str(current_line/total_lines*100)}%')

                tokens = split_to_words(line)

                for token in tokens:
                    if token not in current_batch:
                        continue

                    vectors[token][current_line] = vectors[token][current_line] + 1

                current_line = current_line + 1

        print('Saving vectors')
        save_vectors(vectors, batch_id, chunk_size)
        print('Saved vectors')
        with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
            progress_file.write(str(-1))
            progress_file.flush()
            fsync(progress_file)
