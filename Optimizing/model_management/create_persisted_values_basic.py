# Runnable script calculating values for each dataset for each method and persisting them
# Already persisted values are not calculated again nor persisted

# Mandatory if we want to run this script from windows cmd. Must precede all imports from this project
import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from model_management.sts_method_pool import sts_method_pool
from dataset_modification_scripts.dataset_pool import dataset_pool, find_dataset_by_name
from dataset_modification_scripts.lemmatize.lemmatizer_wrapper import Lemmatizer


# Function to check if two dicts contain the same keys and values.
# Params: dict<str, any>, dict<str, any>
# Return: bool
def dict_match(dict1, dict2):

    for key in dict1:
        if key not in dict2:
            return False
        if dict1[key] != dict2[key]:
            return False

    for key in dict2:
        if key not in dict1:
            return False
        if dict1[key] != dict2[key]:
            return False

    return True


# For each dataset version (raw vs. lemma)
for key in dataset_pool:
    # Loop over each dataset to calculate and persist values for all methods
    for dataset in dataset_pool[key]:

        print('Processing dataset {}'.format(dataset.name))

        # Persist gold standard first - no need to calculate anything
        dataset.persist_gold_standard()

        # Prepare the cache - to avoid loading resources multiple times
        cache = {
            'lemmatizer': Lemmatizer(root_path)
        }

        # Loop over each method we know.
        for sts_method_name in sts_method_pool:
            for sts_method in sts_method_pool[sts_method_name]:
                # If we are dealing with lematized dataset, let's adjust corpora name in args,
                # if the method is vector-based
                if 'corpus' in sts_method.args:
                    if 'lemma' in dataset.name:
                        sts_method.args['corpus'] = sts_method.args['corpus'].replace('_sk.txt', '_sk_lemma.txt')
                    else:
                        sts_method.args['corpus'] = sts_method.args['corpus'].replace('_sk_lemma.txt', '_sk.txt')
                else:
                    dataset.predict_and_persist_values(sts_method, cache)
