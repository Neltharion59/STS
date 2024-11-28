search_query_word = "{0} language:sk loc:sk"
search_query_near = "{0} NEAR:10 {1} language:sk loc:sk"

from time import sleep
from random import randint

import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)
from util.bing import search_result_count
from util.search_register import SearchRegister
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words
from dataset_modification_scripts.dataset_pool import dataset_pool

subpath_data_single_words = 'resources/search_bing_single_words.txt'
subpath_progress_single_words = 'resources/temp/progress_search_bing_single_words.txt'

subpath_data_word_couples_pattern = 'resources/search_bing_word_couples_and_{0}.txt'

with open(os.path.join(root_path, 'resources/stop_words.txt'), 'r', encoding='utf-8') as file:
    stop_words = file.readline().replace(' ', '').split(',')

vector_words = [word for word in get_unique_dataset_words() if word not in stop_words]


def calc_single_words():
    print("Starting to calc for single words")
    register = SearchRegister('bing_single_words')

    for i in range(0, len(vector_words)):
        word = vector_words[i]
        query = search_query_word.format(word)

        if register.contains(query):
            continue

        sleep(randint(50, 1050)/1000)
        result_count = search_result_count(query)
        register.add(query, result_count)

        print(f'Calc single words: \'{query}\'. {i}/{len(vector_words)}. {i / len(vector_words) * 100}%')

        if i % 10 == 0:
            print('Persisting')
            register.persist()

    register.persist()
    print("Finished calcing for single words")


def calc_word_couples():
    print("Starting to calc for word couples")
    register = SearchRegister('bing_word_couples')

    for dataset in dataset_pool['lemma']:
        sentences1, sentences2 = dataset.load_dataset()

        for i in range(0, len(sentences1)):
            print(f'Calc sentences word couples: {i}/{len(sentences1)}. {i / len(sentences1) * 100}%')

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

                    query = search_query_near.format(w1, w2)

                    if register.contains(query):
                        continue

                    result_count = search_result_count(query)
                    register.add(query, result_count)

            register.persist()

    print("Finished calcing for word couples")


calc_single_words()
calc_word_couples()
