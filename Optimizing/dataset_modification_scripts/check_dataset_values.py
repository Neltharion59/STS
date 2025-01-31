import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps

from dataset_modification_scripts.dataset_pool import dataset_pool

for dataset_version in dataset_pool:
    for dataset in dataset_pool[dataset_version]:
        values = dataset.load_values()

        print(dumps(values, indent=4).split('\n')[:30])