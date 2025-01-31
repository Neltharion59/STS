import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import math

from dataset_modification_scripts.dataset_pool import dataset_pool

for dataset_version in dataset_pool:
    for dataset in dataset_pool[dataset_version]:
        values = dataset.load_values()

        for method in values:
            if method == 'gold_standard':
                continue

            for config in values[method]:
                vector = [float(x) for x in config['values']]

                issues = False
                if max(vector) > 1.0:
                    print('MAX Issues with ', method)
                    issues = True

                if min(vector) < 0.0:
                    print('MIN Issues with ', method)
                    issues = True

                if len([math.isnan(x) for x in vector]) > 0:
                    print('NAN Issues with ', method)
                    issues = True

                if issues:
                    continue
