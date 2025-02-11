import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps, loads

from basic_similarity_methods.vector_based import vector_distance
from dataset_modification_scripts.dataset_pool import dataset_pool
from dataset_modification_scripts.dataset_wrapper import gold_standard_name
from model_management.sts_method_pool import args_openai
from util.file_handling import read, write

# We don't need the lemma part
del dataset_pool['lemma']

distance_metrics = args_openai['distance_metric']
openai_models = args_openai['version']

path_to_openai_embeddings_pattern = './resources/vector/open_ai_datasets_text-embedding-{0}_{1}_lemma.txt'

result = {}

for dataset in dataset_pool['raw']:
    result[dataset.name] = {}

    labels = dataset.load_values()[gold_standard_name][0]['values']

    for openai_model in openai_models:
        result[dataset.name][openai_model] = {}
        path_to_openai_embeddings = path_to_openai_embeddings_pattern.format(openai_model.replace('word_', ''), dataset.name.replace('stsb', 'sts-b'))

        vector_pairs = [line.split('\t') for line in read(path_to_openai_embeddings).split('\n') if len(line) > 0]
        vector_pairs = [[loads(vector_pair[0]), loads(vector_pair[1])] for vector_pair in vector_pairs]

        for distance_metric in distance_metrics:
            distances = [vector_distance(vector_pair[0], vector_pair[1], distance_metric) for vector_pair in vector_pairs]

            dist_min = min(distances)
            if dist_min < 0.0:
                distances = [dist + dist_min for dist in distances]

            dist_max = max(distances)
            if dist_max > 1.0:
                distances = [dist/dist_max for dist in distances]

            similarities = [1 - dist for dist in distances]

            result[dataset.name][openai_model][distance_metric] = similarities

write('./resources/openai_embedding_results_full.json', dumps(result))
