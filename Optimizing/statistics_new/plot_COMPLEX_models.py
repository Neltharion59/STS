import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import loads, dumps

from util.file_handling import read
from evaluation.evaluate_regression_metrics import pearson
from dataset_modification_scripts.dataset_pool import dataset_pool
from model_management.sts_method_pool import sts_method_pool
from dataset_modification_scripts.dataset_wrapper import dict_match
from model_management.sts_model_pool import model_types as sts_model_pool
from complex_similarity_methods.dataset_fragmentation_03 import FragmentedDatasetSuper

print('Start')

sts_model_pool = {x['name']: x for x in sts_model_pool}

file_path = './resources/optimizer_runs_final/optimizer_run_final.json'
results = loads(read(file_path))['main']

split_dataset_file_pattern = 'resources/split_datasets/split_dataset_{0}_{1}_sk.json'

model_names = list(sts_model_pool.keys())
dataset_names = list([x.name for x in dataset_pool['raw']])
pearsons = {}

for dataset_version in dataset_pool:
    print('Dataset version:', dataset_version)
    pearsons[dataset_version] = {}

    for dataset in dataset_pool[dataset_version]:
        print('\tDataset:', dataset.name)
        dataset_names.append(dataset.name)

        pearsons[dataset_version][dataset.name] = {}

        split_dataset_master_json = loads(read(split_dataset_file_pattern.format(dataset.name, dataset_version)))

        split_dataset_master = FragmentedDatasetSuper()
        split_dataset_master.from_json(split_dataset_master_json)

        for model_name in results[dataset_version][dataset.name]['models']:
            print('\t\tModel:', model_name)

            model_stats = results[dataset_version][dataset.name]['models'][model_name]['best_model']

            feature_indices = []
            for arg_item1 in model_stats['inputs']:
                # TODO - compatibility
                if 'wordnet' in arg_item1['args']:
                    arg_item1['args']['wordnet'] = 'omw-sk:1.4'

                print('\t\tMatching', arg_item1['args'])
                i = 0
                added = False
                for arg_item2 in sts_method_pool[arg_item1['method_name']]:
                    print('\t\t\tWith', arg_item2.args)

                    if dict_match(arg_item1['args'], arg_item2.args):
                        added = True
                        feature_indices.append({
                            'method_name': arg_item1['method_name'],
                            'arg_index': i
                        })
                        break

                    i = i + 1

                if not added:
                    raise ValueError('No matching dict')

            train_set = split_dataset_master.Train.produce_subset(feature_indices)
            validation_set = split_dataset_master.Validation.produce_subset(feature_indices)


            # TODO - compatibility
            #if model_name == 'decision_tree_regression':
            #    if 'max_features' in model_stats['hyperparams']:
            #        del model_stats['hyperparams']['max_features']

            print('\t\tFitting:', model_name)
            model = sts_model_pool[model_name]['model'](**model_stats['hyperparams'])

            model.fit(train_set.features[0], train_set.labels)

            print('\t\tValidating:', model_name)
            pearson_train = model_stats['pearson']
            pearson_validation = pearson(validation_set.labels, model.predict(validation_set.features[0]))

            pearsons[dataset_version][dataset.name][model_name] = {
                'train': pearson_train,
                'validate': pearson_validation
            }

print((dumps(pearsons, indent=4)))
