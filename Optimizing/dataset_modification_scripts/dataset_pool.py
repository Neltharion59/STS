# Library-like script providing pool of wrappers of all defined datasets
# Dataset is defined by its name and sub-datasets
import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from dataset_modification_scripts.dataset_wrapper import Dataset

dataset_pool = {
    'raw': [
        Dataset(
            "stsbenchmark",
            [
                "stsbenchmark_sk.txt"
            ]
        ),
        Dataset(
            "sick",
            [
                "sick_sk.txt"
            ]
        )
    ]
}
# Create equivalent lematized entries
dataset_pool['lemma'] = [
    Dataset
    (
        dataset.name + "_lemma",
        [dataset_name.replace('_sk.txt', '_sk_lemma.txt') for dataset_name in dataset.dataset_names]
    )
    for dataset in dataset_pool['raw']
]


# Handy function to find dataset in pool with given name.
# Params: str, str
# Return: Dataset | None
def find_dataset_by_name(key, dataset_name):
    for dataset in dataset_pool[key]:
        if dataset.name == dataset_name:
            return dataset

    return None
