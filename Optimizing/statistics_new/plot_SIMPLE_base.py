import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps
from functools import reduce

from dataset_modification_scripts.dataset_pool import dataset_pool
from dataset_modification_scripts.dataset_wrapper import gold_standard_name
from evaluation.evaluate_regression_metrics import pearson
from statistics_new.significance_test_raw_vs_lemma_base import test_significance


def get_values(method_list, inverse=False):
    def normalize(numbers, inverse):
        normalized_numbers = [max(0, x) for x in numbers]
        upper_cap = max(normalized_numbers)

        if upper_cap > 1.0:
            normalized_numbers = [x/upper_cap for x in normalized_numbers]

        if inverse:
            normalized_numbers = [1 - x for x in normalized_numbers]

        return normalized_numbers

    results = {
        'x': list(range(len(method_list))),
        'x_labels': method_list,
        'datasets': {}
    }

    for dataset_version in dataset_pool:

        for dataset in dataset_pool[dataset_version]:
            dataset_name = dataset.name.replace('_lemma', '')

            if dataset_name not in results['datasets']:
                results['datasets'][dataset_name] = {}

            dataset_values = dataset.load_values()

            gold_standard = dataset_values[gold_standard_name][0]['values']
            if max(gold_standard) > 1.0:
                gold_standard = [x/5 for x in gold_standard]

            for method_name in method_list:
                pearson_value = max([pearson(gold_standard, normalize(dataset_values[method_name][i]['values'], inverse)) for i in range(len(dataset_values[method_name]))])

                if dataset_version not in results['datasets'][dataset_name]:
                    results['datasets'][dataset_name][dataset_version] = []

                results['datasets'][dataset_name][dataset_version].append(pearson_value)

    return results


def print_values(results):
    output_lines = []
    for dataset_name in results['datasets']:
        output_lines.append('# {0}'.format(dataset_name))
        output_lines.append('x = [{0}]'.format(', '.join([str(x) for x in results['x']])))
        output_lines.append('y1 = [{0}]'.format(', '.join([str(x) for x in results['datasets'][dataset_name]['raw']])))
        output_lines.append('y2 = [{0}]'.format(', '.join([str(x) for x in results['datasets'][dataset_name]['lemma']])))
        output_lines.append('x_labels = [{0}]'.format(', '.join(['\'{0}\''.format(x) for x in results['x_labels']])))
        output_lines.append('-' * 30)

    print('\n'.join(output_lines))


def test_lemma_significance(results):
    print('-' * 30)

    raw_values = reduce(lambda a, b: a + b, [results['datasets'][dataset_name]['raw'] for dataset_name in results['datasets']])
    lemma_values = reduce(lambda a, b: a + b, [results['datasets'][dataset_name]['lemma'] for dataset_name in results['datasets']])
    p_value = 0.05

    lemma_significacy = test_significance(raw_values, lemma_values, p_value)
    print(dumps(lemma_significacy, indent=4))