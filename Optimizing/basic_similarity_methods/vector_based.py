# Library-like script providing vector-based similarity methods (along with function to turn text to vector)
import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import load, loads
from operator import add
from functools import reduce
from itertools import chain
from scipy.spatial.distance import cosine as cos, cityblock as manhattan, euclidean, minkowski, braycurtis, canberra, chebyshev, correlation, jensenshannon
from corpora_modification_scripts.Util import split_to_words
from util.file_handling import read
from corpora_modification_scripts.Util import get_unique_dataset_words

# Arg possibilities for vector-based methods
args_vector_based = {
    'vector_merge_strategy': ['add', 'add_pos_weight', 'add_power11_weight', 'concat_pad', 'concat_cutoff'],
    'missing_vector_strategy': ['skip', 'zeroes'],
    'normalize_word_vector_length_strategy': ['pad', 'cutoff']
}
unique_dataset_words = get_unique_dataset_words()


def hal(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vector_subtype' not in cache or 'vectors' not in cache or cache['vector_type'] != 'hal' or cache['vector_subtype'] != args['size'] or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'hal'
        cache['vector_subtype'] = args['size']
        # Load the vectors
        if 'size' not in args:
            raise ValueError('Size not present in args when calculating with HAL vectors')

        args['size'] = '300'
        if args['size'] == 'full':
            file_path = './resources/vector/hal_full.json'
        elif args['size'] in ['100', '200', '300', '400', '500', '600', '700', '800']:
            file_path = './resources/vector/hal_svd_{0}.json'.format(args['size'])
        else:
            raise ValueError('Unknown \'size\' of HAL vectors: {0}'.format(args['size']))

        cache['vectors'] = loads(read(file_path))

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def lsa(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vectors' not in cache or cache['vector_type'] != 'lsa' or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'lsa'
        # Load the vectors
        cache['vectors'] = load_lsa_vectors(text1, text2, cache)

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def esa(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vectors' not in cache or cache['vector_type'] != 'esa' or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'esa'
        # Load the vectors
        vectors = loads(read('./resources/vector/esa_v1_full.txt'))
        vectors = {key: [float(num) for num in vectors[key].split(',')] for key in vectors}
        cache['vectors'] = vectors

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def disco(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vector_subtype' not in cache or 'vectors' not in cache or cache['vector_type'] != 'disco' or cache['vector_subtype'] != args['version'] or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'disco'
        cache['vector_subtype'] = args['version']
        # Load the vectors
        if args['version'] == 'raw':
            file_path = './resources/vector/disco_raw.txt'
            lines = read(file_path).split('\n')
            vectors = {line.split('\t')[0]: [float(num) for num in line.split('\t')[1]] for line in lines}
            cache['vectors'] = vectors
        elif args['version'] in ['so_5', 'so_10', 'so_15']:
            file_path_raw = './resources/vector/disco_raw.txt'
            lines_raw = read(file_path_raw).split('\n')
            vectors_raw = {line.split('\t')[0]: [float(num) for num in line.split('\t')[1]] for line in lines_raw}

            file_path_ordered_sims = './resources/vector/disco_lin_sims.json'
            sims = loads(read(file_path_ordered_sims))
            sim_word_count = int(args['version'].replace('so_', ''))

            vectors = {word: [x['word'] for x in sims[word][:sim_word_count]] for word in vectors_raw}
            vectors = {word: reduce(lambda a, b: a+b, [vectors_raw[w2] for w2 in vectors[word]], []) for word in vectors}

            cache['vectors'] = vectors
        else:
            raise ValueError('Unknown \'version\' of DISCO vectors: {0}'.format(args['version']))

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def openai(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vector_subtype' not in cache or 'vectors' not in cache or cache['vector_type'] != 'openai' or cache['vector_subtype'] != args['version'] or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'openai'
        cache['vector_subtype'] = args['version']
        # Load the vectors
        if args['version'] in ['word_3-small', 'word_3-large', 'word_ada-002']:
            file_path = './resources/vector/open_ai_words_text-embedding-{0}.txt'.format(args['version'].replace('word_', ''))
            vectors = loads(read(file_path))
            cache['vectors'] = vectors
        else:
            raise ValueError('Unknown \'version\' of OPEN-AI vectors: {0}'.format(args['version']))

    v1, v2 = vectorize_text(text1, text2, args, cache)
    distance = vector_distance(v1, v2, args['distance_metric'])

    return distance


def fast_text(text1, text2, args, cache):
    if 'vector_type' not in cache or 'vectors' not in cache or cache['vector_type'] != 'fast_text' or cache['vectors'] is None:
        cache['vectors'] = None
        cache['vector_type'] = 'fast_text'
        # Load the vectors
        file_path = './resources/vector/fast_text_classic.json'
        vectors = loads(read(file_path))
        cache['vectors'] = vectors

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

    word_vectors1 = list(map(lambda w: cache['vectors'][w] if w in cache['vectors'] else [], words1))
    word_vectors2 = list(map(lambda w: cache['vectors'][w] if w in cache['vectors'] else [], words2))

    if args['normalize_word_vector_length_strategy'] == 'pad':
        vector_length = reduce(max, [len(v) for v in (word_vectors1 + word_vectors2)])
        word_vectors1 = [(v + [0] * (vector_length - len(v))) if len(v) > 0 else [] for v in word_vectors1]
        word_vectors2 = [(v + [0] * (vector_length - len(v))) if len(v) > 0 else [] for v in word_vectors2]
    elif args['normalize_word_vector_length_strategy'] == 'cutoff':
        vector_length = reduce(min, [len(v) for v in chain(word_vectors1, word_vectors2) if len(v) > 0])
        word_vectors1 = [v[:vector_length] if len(v) > 0 else [] for v in word_vectors1]
        word_vectors2 = [v[:vector_length] if len(v) > 0 else [] for v in word_vectors2]
    else:
        raise ValueError('Unknown normalize_word_vector_length_strategy: {0}'.format(args['normalize_word_vector_length_strategy']))

    #vector_length = len(cache['vectors'][list(cache['vectors'].keys())[0]])

    if args['missing_vector_strategy'] == 'skip':
        pass
    elif args['missing_vector_strategy'] == 'zeroes':
        word_vectors1 = [v if len(v) > 0 else [0] * vector_length for v in word_vectors1]
        word_vectors2 = [v if len(v) > 0 else [0] * vector_length for v in word_vectors2]
    else:
        raise ValueError('Unknown missing_vector_strategy: {0}'.format(args['missing_vector_strategy']))

    if args['vector_merge_strategy'] == 'add':
        word_vectors1 = [v for v in word_vectors1 if len(v) > 0]
        word_vectors2 = [v for v in word_vectors2 if len(v) > 0]

        vector1 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors1, [0] * vector_length)
        vector2 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors2, [0] * vector_length)

    elif args['vector_merge_strategy'] == 'add_pos_weight':
        word_vectors1 = [[x * (i+1) for x in v] for v, i in zip(word_vectors1, range(len(word_vectors1)))]
        word_vectors2 = [[x * (i+1) for x in v] for v, i in zip(word_vectors2, range(len(word_vectors2)))]

        word_vectors1 = [v for v in word_vectors1 if len(v) > 0]
        word_vectors2 = [v for v in word_vectors2 if len(v) > 0]

        vector1 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors1, [0] * vector_length)
        vector2 = reduce(lambda a,b: [a[i]+b[i] for i in range(len(a))], word_vectors2, [0] * vector_length)

    elif args['vector_merge_strategy'] == 'add_power11_weight':
        word_vectors1 = [[x * (11**i) for x in v] for v, i in zip(word_vectors1, range(len(word_vectors1)))]
        word_vectors2 = [[x * (11**i) for x in v] for v, i in zip(word_vectors2, range(len(word_vectors2)))]

        word_vectors1 = [v for v in word_vectors1 if len(v) > 0]
        word_vectors2 = [v for v in word_vectors2 if len(v) > 0]

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
    elif distance_metric == 'cosine':
        return cos(vector1, vector2)
    else:
        raise ValueError('Unknown distance_metric: {0}'.format(distance_metric))


# .....yeah.
def load_lsa_vectors(text1, text2, cache):
    lemma1 = cache['lemmatizer'].lemmatize(text1)
    lemma2 = cache['lemmatizer'].lemmatize(text2)

    words = list(set(split_to_words(lemma1) + split_to_words(lemma2)))
    indices = sorted([{'word': word, 'index': unique_dataset_words.index(word)} for word in words], key=lambda x: x['index'])

    for item in indices:
        item['batch_id'] = int(item['index']//1000)

    for batch_id in range(18):
        batch_items = [item for item in indices if item['batch_id'] == batch_id]
        batch_indices = [item['index'] for item in batch_items]

        if len(batch_items) == 0:
            continue

        with open('./resources/vector/lsa_full_{0}_1000.txt'.format(batch_id), 'r', encoding='utf-8') as lsa_file:
            i = 0
            j = 0
            for line in lsa_file:
                if i == batch_indices[j]:
                    vector = [int(x) for x in line.replace('\n', '').split('\t')[1].split(',')]
                    batch_items[j]['vector'] = vector
                    j = j + 1

                    if j >= len(batch_items):
                        continue

                i = i + 1

    if len([item for item in indices if 'vector' not in item]) > 0:
        raise ValueError('No LSA vectors found for items: {0}'.format([item for item in indices if 'vector' not in item]))

    vectors = {item['word']: item['vector'] for item in indices}

    return vectors

