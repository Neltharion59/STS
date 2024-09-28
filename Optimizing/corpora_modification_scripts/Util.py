import re
import time
from dataset_modification_scripts.dataset_pool import dataset_pool


def split_to_words(line):
    tokens = re.split('\W+', line)
    tokens = [token.lower()[:30] for token in tokens]
    tokens = [token for token in tokens if token.isalpha()]
    return tokens


def get_unique_dataset_words():
    datasets = dataset_pool['lemma']
    all_words = {}
    for dataset in datasets:
        left_lines, right_lines = dataset.load_dataset()
        lines = left_lines + right_lines
        for line in lines:
            words = split_to_words(line)
            for word in words:
                if word not in all_words:
                    all_words[word] = 0
    return all_words


def get_feature_words():
    feature_word_file = './../resources/feature_words.txt'
    with open(feature_word_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.split()[0] for line in lines if len(line.split()[0]) > 1]


def get_stop_words():
    stop_word_file = './../resources/stop_words.txt'
    with open(stop_word_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines[0].split()


def get_non_stop_feature_words():
    return list(set(get_feature_words()) - set(get_stop_words()))
