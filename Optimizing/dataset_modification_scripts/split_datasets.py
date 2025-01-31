import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps

from complex_similarity_methods.dataset_fragmentation import FragmentedDatasetSuper
from complex_similarity_methods.dataset_split_ratio import DatasetSplitRatio
from dataset_modification_scripts.dataset_wrapper import gold_standard_name
from dataset_modification_scripts.dataset_pool import dataset_pool
from util.file_handling import write, exists

dataset_file_pattern = 'resources/split_datasets/split_dataset_{0}_{1}_sk.json'

dataset_split_ratio = DatasetSplitRatio(0.80, 0.20)

# Lemma vs. Raw
for key in dataset_pool:
    # For each dataset
    for dataset in dataset_pool[key]:
        dataset_path = dataset_file_pattern.format(dataset.name, key)

        if exists(dataset_path):
            continue

        persisted_methods_temp = dataset.load_values()
        gold_values_temp = [round(x / 5, ndigits=3) for x in persisted_methods_temp[gold_standard_name][0]['values']]
        del persisted_methods_temp[gold_standard_name]

        split_dataset_master = FragmentedDatasetSuper()
        split_dataset_master.from_full_dataset(persisted_methods_temp, gold_values_temp, dataset_split_ratio)

        split_dataset_json = {
            'DatasetName': dataset.name,
            'DatasetVersion': key,
            'Language': 'sk',
            'TrainRatio': dataset_split_ratio.train_ratio,
            'Train': {
                'features': split_dataset_master.Train.features,
                'labels': split_dataset_master.Train.labels
            },
            'Validate': {
                'features': split_dataset_master.Validation.features,
                'labels': split_dataset_master.Validation.labels
            }
        }

        write(dataset_path, dumps(split_dataset_json, indent=4))
