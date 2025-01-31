import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from dataset_modification_scripts.dataset_pool import dataset_pool

for dataset_version in dataset_pool:
    for dataset in dataset_pool[dataset_version]:
        values = dataset.load_values()

        for method in values:
            if method == 'gold_standard':
                continue

            for config in values[method]:
                if max([float(x) for x in config['values']]) > 1.0 or min([float(x) for x in config['values']]) < 0.0:
                    print('Issues with ', method, ' - ', config['args'])
