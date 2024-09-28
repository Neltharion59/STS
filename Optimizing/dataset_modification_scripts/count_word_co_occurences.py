import sys
import os
conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from os import listdir, fsync
from os.path import isfile, join
import re
import math
from json import loads, dumps
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words


dataset_words = get_unique_dataset_words()


def is_interesting_word(word):
    return word in dataset_words


def to_words(line):
    tokens = re.split('\W+', line)
    return [token.lower()[:30] for token in tokens]


def get_corpus_file_id(corpus_file_name):
    return corpus_file_name.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')


corpora_directory_path = './../resources/corpora/processed/'

corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = sorted([x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)], key=lambda x: int(get_corpus_file_id(x)))
corpus_progress_track_file_name_pattern = "progress_co_occurence_oscarsk_{}"


word_occurence_file_path = './../resources/word_occurences.json'
word_co_ccurence_file_path = './../resources/word_co_occurences.json'

try:
    with open(word_occurence_file_path, 'r', encoding='utf-8') as word_occurence_file:
        temp = word_occurence_file.read()
    total_word_occurences = loads(temp)
except FileNotFoundError:
    total_word_occurences = {}

try:
    with open(word_co_ccurence_file_path, 'r', encoding='utf-8') as word_co_occurence_file:
        temp = word_co_occurence_file.read()
    co_occurences = loads(temp)
except FileNotFoundError:
    co_occurences = {}

for input_corpus_file in input_corpus_files:
    corpus_file_path = join(corpora_directory_path, input_corpus_file)
    dataset_part_id = corpus_file_path.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')
    progress_file_path = './../resources/temp/' + corpus_progress_track_file_name_pattern.format(dataset_part_id) + '.txt'

    print("-"*30)
    print(f"[{input_corpus_file}] Processing")

    last_processed_line = 0
    try:
        with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
            last_processed_line = int(progress_file.read())
    except FileNotFoundError:
        pass

    if last_processed_line == -1:
        print(f"[{input_corpus_file}] Corpus already processed")
        continue

    print(f"[{input_corpus_file}] Counting lines")
    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        total_lines = len(corpus_file.readlines())


    print(f"[{input_corpus_file}] Opening the file")
    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        k = 0
        print(f"[{input_corpus_file}] Starting to process the first line ")
        for line in corpus_file:
            k = k + 1
            print(f"[{input_corpus_file}] Processing line {k}/{total_lines} ({str(round(k/total_lines * 100, 6))}%).")

            words = split_to_words(line)

            for i in range(len(words)):
                if words[i] not in dataset_words:
                    continue

                if words[i] not in total_word_occurences:
                    total_word_occurences[words[i]] = 1
                else:
                    total_word_occurences[words[i]] = total_word_occurences[words[i]] + 1

                for j in range(i, len(words)):
                    if words[i] == words[j]:
                        continue

                    if words[j] not in dataset_words:
                        continue

                    pair = sorted([words[i], words[j]])

                    if pair[0] not in co_occurences:
                        co_occurences[pair[0]] = {}
                    if pair[1] not in co_occurences[pair[0]]:
                        co_occurences[pair[0]][pair[1]] = 0
                    co_occurences[pair[0]][pair[1]] = co_occurences[pair[0]][pair[1]] + 1

    texts = []

    print(f"[{input_corpus_file}] Saving total word occurences")
    temp = dumps(total_word_occurences)
    with open(word_occurence_file_path, 'w+', encoding='utf-8') as word_occurence_file:
        word_occurence_file.write(temp)
        word_occurence_file.flush()
        fsync(word_occurence_file)

    print(f"[{input_corpus_file}] Saving total word co-occurences")
    temp = dumps(co_occurences)
    with open(word_co_ccurence_file_path, 'w+', encoding='utf-8') as word_co_occurence_file:
        word_co_occurence_file.write(temp)
        word_co_occurence_file.flush()
        fsync(word_co_occurence_file)

    print(f"[{input_corpus_file}] Saving progress file")
    with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
        progress_file.write(str(-1))
        progress_file.flush()
        fsync(progress_file)

