import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import loads
from math import log2
from corpora_modification_scripts.Util import split_to_words
from util.file_handling import read
from util.math import average

args_pmi = {
    'merge_strategy': ['each', 'positional'],
    'aggregation_strategy': ['avg', 'max', 'min']
}

def pmi(text1, text2, args, cache):
    lemma1 = cache['lemmatizer'].lemmatize(text1)
    lemma2 = cache['lemmatizer'].lemmatize(text2)

    words1 = split_to_words(lemma1)
    words2 = split_to_words(lemma2)

    if 'word_occurences' not in cache:
        cache['word_occurences'] = loads(read('./resources/word_occurences.json'))
    if 'word_co_occurences' not in cache:
        cache['word_co_occurences'] = loads(read('./resources/word_co_occurences.json'))

    if args['merge_strategy'] == 'each':
        similarities = [pmi_single(w1, w2, cache) for w1 in words1 for w2 in words2]
    elif args['merge_strategy'] == 'positional':
        similarities = [pmi_single(words1[i], words2[i], cache) for i in range(min(len(words1), len(words2)))]
    else:
        raise ValueError('Unknown merge_strategy: {0}'.format(args['merge_strategy']))

    if args['aggregation_strategy'] == 'avg':
        result = average(similarities)
    elif args['aggregation_strategy'] == 'max':
        result = max(similarities)
    elif args['aggregation_strategy'] == 'min':
        result = min(similarities)
    else:
        raise ValueError('Unknown aggregation_strategy: {0}'.format(args['aggregation_strategy']))

    return result


def pmi_single(w1, w2, cache):
    occurence1 = cache['word_occurences'][w1]
    occurence2 = cache['word_occurences'][w2]

    if w1 in cache['word_occurences'] and w2 in cache['word_occurences'][w1]:
        co_occurence = cache['word_co_occurences'][w1][w2]
    elif w2 in cache['word_occurences'] and w1 in cache['word_occurences'][w2]:
        co_occurence = cache['word_co_occurences'][w2][w1]
    else:
        co_occurence = 0

    normalized_to_minus1_1 = max(0, log2(co_occurence/(occurence1 * occurence2)))/log2(co_occurence) if log2(co_occurence) != 0 else 0
    normalized_to_0_1 = (normalized_to_minus1_1 + 1)/2
    return normalized_to_0_1
