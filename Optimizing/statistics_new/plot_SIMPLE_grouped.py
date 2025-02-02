import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from model_management.sts_method_pool import string_based_name_list, corpus_based_name_list, knowledge_based_name_list
from statistics_new.plot_SIMPLE_base import get_values, print_values


results_string = get_values(string_based_name_list)
results_corpus = get_values(corpus_based_name_list, inverse=True)
results_knowledge = get_values(knowledge_based_name_list)

results_merged = {
    'x': list(range(3)),
    'x_labels': ['string', 'statistical', 'knowledge'],
    'datasets': {}
}

for dataset_name in results_string['datasets']:
    results_merged['datasets'][dataset_name] = {}

    for dataset_version in results_string['datasets'][dataset_name]:
        results_merged['datasets'][dataset_name][dataset_version] = [
            max(results_string['datasets'][dataset_name][dataset_version]),
            max(results_corpus['datasets'][dataset_name][dataset_version]),
            max(results_knowledge['datasets'][dataset_name][dataset_version]),
        ]

print_values(results_merged)
