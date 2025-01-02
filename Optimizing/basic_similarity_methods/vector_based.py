# Library-like script providing vector-based similarity methods (along with function to turn text to vector)
import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from decimal import Decimal
from math import sqrt
from operator import add
from functools import reduce
from itertools import chain
from scipy.spatial.distance import cosine as cos, cityblock as manhattan, euclidean, minkowski, braycurtis, canberra, chebyshev, correlation, jensenshannon, mahalanobis
from corpora_modification_scripts.Util import split_to_words

# Arg possibilities for vector-based methods
args_vector_based = {
    'vector_merge_strategy': ['add', 'add_pos_weight', 'add_power11_weight', 'concat_pad', 'concat_cutoff'],
    'missing_vector_strategy': ['skip', 'zeroes'],
    'normalize_word_vector_length_strategy': ['pad', 'cutoff']
}


def hal(text1, text2, args, cache):
    if cache['vector_type'] != 'hal' or cache['vectors'] is None:
        cache['vector_type'] = 'hal'
        cache['vectors'] = {} # Load the vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def lsa(text1, text2, args, cache):
    if cache['vector_type'] != 'lsa' or cache['vectors'] is None:
        cache['vector_type'] = 'lsa'
        cache['vectors'] = {} # Load the vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def esa(text1, text2, args, cache):
    if cache['vector_type'] != 'esa' or cache['vectors'] is None:
        cache['vector_type'] = 'esa'
        cache['vectors'] = {} # Load the vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def disco(text1, text2, args, cache):
    if cache['vector_type'] != 'disco' or cache['vectors'] is None:
        cache['vector_type'] = 'disco'
        cache['vectors'] = {} # Load the vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def openai(text1, text2, args, cache):
    if cache['vector_type'] != 'openai' or cache['vectors'] is None:
        cache['vector_type'] = 'openai'
        cache['vectors'] = {} # Load the vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance




# For given strings of text creates vector representation based on args.
# Params: str, str, dict<str, str>
# Return: list<float>, list<float>
def vectorize_text(text1, text2, args, cache):
    lemma1 = cache['lemmatizer'].lemmatize(text1)
    lemma2 = cache['lemmatizer'].lemmatize(text2)

    words1 = split_to_words(lemma1)
    words2 = split_to_words(lemma2)

    word_vectors1 = map(lambda w: cache['vectors'][w] if w in cache['vectors'] else [], words1)
    word_vectors2 = map(lambda w: cache['vectors'][w] if w in cache['vectors'] else [], words2)

    if 'normalize_word_vector_length_strategy' == 'pad':
        vector_length = reduce(max, [len(v) for v in chain(word_vectors1, word_vectors2)])
        word_vectors1 = [(v + [0] * (vector_length - len(v))) if len(v) > 0 else [] for v in word_vectors1]
        word_vectors2 = [(v + [0] * (vector_length - len(v))) if len(v) > 0 else [] for v in word_vectors2]
    elif 'normalize_word_vector_length_strategy' == 'cutoff':
        vector_length = reduce(min, [len(v) for v in chain(word_vectors1, word_vectors2) if len(v) > 0])
        word_vectors1 = [v[:vector_length] if len(v) > 0 else [] for v in word_vectors1]
        word_vectors2 = [v[:vector_length] if len(v) > 0 else [] for v in word_vectors2]
    else:
        raise ValueError('Unknown normalize_word_vector_length_strategy: {0}'.format(args['normalize_word_vector_length_strategy']))

    vector_length = len(cache['vectors'][list(cache['vectors'].keys())[0]])

    if args['missing_vector_strategy'] == 'skip':
        pass
    elif args['missing_vector_strategy'] == 'zeroes':
        word_vectors1 = [v if len(v) > 0 else [0] * vector_length for v in word_vectors1]
        word_vectors2 = [v if len(v) > 0 else [0] * vector_length for v in word_vectors2]
    else:
        raise ValueError('Unknown missing_vector_strategy: {0}'.format(args['missing_vector_strategy']))

    if args['vector_merge_strategy'] == 'add':
        vector1 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors1, [0] * vector_length)
        vector2 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors2, [0] * vector_length)

    elif args['vector_merge_strategy'] == 'add_pos_weight':
        word_vectors1 = [[x * i for x in v] for v, i in zip(word_vectors1, range(len(word_vectors1)))]
        word_vectors2 = [[x * i for x in v] for v, i in zip(word_vectors2, range(len(word_vectors2)))]
        vector1 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors1, [0] * vector_length)
        vector2 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors2, [0] * vector_length)

    elif args['vector_merge_strategy'] == 'add_power11_weight':
        word_vectors1 = [[x * (11**i) for x in v] for v, i in zip(word_vectors1, range(len(word_vectors1)))]
        word_vectors2 = [[x * (11**i) for x in v] for v, i in zip(word_vectors2, range(len(word_vectors2)))]
        vector1 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors1, [0] * vector_length)
        vector2 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors2, [0] * vector_length)

    elif args['vector_merge_strategy'] == 'concat_pad':
        vector1 = reduce(add, word_vectors1)
        vector2 = reduce(add, word_vectors2)

        if len(vector1) < len(vector2):
            vector1 = vector1 + [0] * (len(vector2) - len(vector1))
        elif len(vector1) > len(vector2):
            vector2 = vector2 + [0] * (len(vector1) - len(vector2))

    elif args['vector_merge_strategy'] == 'concat_cutoff':
        vector1 = reduce(add, word_vectors1)
        vector2 = reduce(add, word_vectors2)
        if len(vector1) < len(vector2):
            vector2 = vector2[:len(vector1)]
        elif len(vector1) > len(vector2):
            vector1 = vector1[:len(vector2)]
    else:
        raise ValueError('Unknown vector_merge_strategy: {0}'.format(args['vector_merge_strategy']))

    return vector1, vector2


def vector_distance(vector1, vector2, distance_metric):
    if distance_metric == 'manhattan':
        return manhattan(vector1, vector2)
    elif distance_metric == 'euclidean':
        return euclidean(vector1, vector2)
    elif distance_metric == 'minkowski':
        return minkowski(vector1, vector2, 3)
    elif distance_metric == 'braycurtis':
        return braycurtis(vector1, vector2)
    elif distance_metric == 'canberra':
        return canberra(vector1, vector2)
    elif distance_metric == 'chebyshev':
        return chebyshev(vector1, vector2)
    elif distance_metric == 'correlation':
        return correlation(vector1, vector2)
    elif distance_metric == 'jensenshannon':
        return jensenshannon(vector1, vector2)
    elif distance_metric == 'mahalanobis':
        return mahalanobis(vector1, vector2)
    elif distance_metric == 'cosine':
        return cos(vector1, vector2)
    else:
        raise ValueError('Unknown distance_metric: {0}'.format(distance_metric))
