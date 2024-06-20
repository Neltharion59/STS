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


