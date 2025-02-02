import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import math
from json import loads, dumps

from dataset_modification_scripts.dataset_pool import dataset_pool
from model_management.sts_method_pool import corpus_based_name_list
from util.file_handling import write, read

dataset_file_pattern = 'resources/split_datasets/split_dataset_{0}_{1}_sk.json'

for dataset_version in dataset_pool:
    for dataset in dataset_pool[dataset_version]:

        dataset_file = dataset_file_pattern.format(dataset.name, dataset_version)
        value_object = loads(read(dataset_file))
        object_modified = False

        for dataset_part in ['Train', 'Validate']:
            for method in value_object[dataset_part]['features']:
                if method == 'gold_standard':
                    continue

                for i in range(len(value_object[dataset_part]['features'][method])):

                    vector = value_object[dataset_part]['features'][method][i]['values']
                    modified = False

                    # Clamp negative values
                    if min(vector) < 0.0:
                        vector = [max(0, x) for x in value_object[dataset_part]['features'][method][i]['values']]
                        modified = True

                    # Normalize
                    max_value = max(vector)
                    if max_value > 1.0:
                        vector = [x/max_value for x in vector]
                        modified = True

                    # Vector-based values - They are distances right now, not similarities
                    if method in corpus_based_name_list:
                        vector = [1 - x for x in vector]
                        modified = True

                    if modified:
                        object_modified = True
                        value_object[dataset_part]['features'][method][i]['values'] = vector

        if object_modified:
            write(dataset_file, dumps(value_object, indent=4))
