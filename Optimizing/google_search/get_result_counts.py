search_query_near = "{0} NEAR:10 {1} language:sk loc:sk"

from json import loads, dumps
from time import sleep
from random import randint

import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)
from util.bing import search_result_count
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words
from util.file_handling import read, write
from dataset_modification_scripts.dataset_pool import dataset_pool

subpath_data_single_words = 'resources/search_bing_single_words.txt'
subpath_progress_single_words = 'resources/temp/progress_search_bing_single_words.txt'

subpath_data_word_couples_pattern = 'resources/search_bing_word_couples_and_{0}.txt'

with open(os.path.join(root_path, 'resources/stop_words.txt'), 'r', encoding='utf-8') as file:
    stop_words = file.readline().replace(' ', '').split(',')

vector_words = [word for word in get_unique_dataset_words() if word not in stop_words]


def calc_single_words():
    try:
        result_counts = loads(read(subpath_data_single_words))
    except FileNotFoundError:
        result_counts = {}

    print("Starting to calc for single words")
    for i in range(0, len(vector_words)):
        word = vector_words[i]

        if word in result_counts and result_counts[word] != 0:
            if i % 100 == 0:
                print(f'Already owned: \'{word}\'. {i}/{len(vector_words)}. {i / len(vector_words) * 100}%')
            continue

        sleep(randint(50, 1050)/1000)
        result_count = search_result_count(word)
        result_counts[word] = result_count

        if i % 20 == 0:
            print(f'Calc single words: \'{word}\'. {i}/{len(vector_words)}. {i / len(vector_words) * 100}%')
            data = dumps(result_counts)
            write(subpath_data_single_words, data)

    data = dumps(result_counts)
    write(subpath_data_single_words, data)


def calc_word_couples():

    for dataset in dataset_pool['lemma']:
        subpath_data_word_couples = subpath_data_word_couples_pattern.format(dataset.name)
        try:
            result_counts = loads(read(subpath_data_word_couples))
        except FileNotFoundError:
            result_counts = {}

        sentences1, sentences2 = dataset.load_dataset()

        for i in range(0, len(sentences1)):
            print(f'Calc sentences word couples: {i}/{len(vector_words)}. {i / len(vector_words) * 100}%')

            words1 = split_to_words(sentences1[i])
            words2 = split_to_words(sentences2[i])

            for word1 in words1:
                if word1 in stop_words:
                    continue

                for word2 in words2:
                    if word1 == word2:
                        continue

                    if word2 in stop_words:
                        continue

                    w1 = word1
                    w2 = word2

                    if w2 < w1:
                        w1 = word2
                        w2 = word1

                    if w1 not in result_counts:
                        result_counts[w1] = {}
                    if w2 in result_counts[w1] and result_counts[w1][w2] != 0:
                        continue

                    search_query = search_query_near.format(w1, w2)
                    result_count = search_result_count(search_query)
                    result_counts[w1][w2] = result_count

            data = dumps(result_counts)
            write(subpath_data_word_couples, data)

        data = dumps(result_counts)
        write(subpath_data_word_couples, data)


calc_single_words()
calc_word_couples()
