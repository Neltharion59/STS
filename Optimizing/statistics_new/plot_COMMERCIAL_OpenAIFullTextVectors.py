import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import loads, dumps

from util.math import average
from util.file_handling import read
from evaluation.evaluate_regression_metrics import spearman
from dataset_modification_scripts.dataset_pool import dataset_pool
from dataset_modification_scripts.dataset_wrapper import gold_standard_name
from statistics_new.significance_test_raw_vs_lemma_base import test_significance

file_path = './resources/openai_embedding_results_full.json'

results = loads(read(file_path))
pearsons = {}
model_names = []
metric_names = []
dataset_names = []

for dataset in dataset_pool['raw']:
    dataset_names.append(dataset.name)

    pearsons[dataset.name] = {}
    labels = dataset.load_values()[gold_standard_name][0]['values']

    for model_name in results[dataset.name]:
        pearsons[dataset.name][model_name] = {}

        for distance_metric_name in results[dataset.name][model_name]:
            pearsons[dataset.name][model_name][distance_metric_name] = spearman(labels, results[dataset.name][model_name][distance_metric_name])

    model_names = list(results[dataset.name].keys())
    metric_names = list(results[dataset.name][model_names[0]].keys())

print('-' * 30)
print('Group by model')
print('-' * 30)
group_by_model = {model_name: [] for model_name in model_names}
for dataset_name in dataset_names:
    for model_name in model_names:
        for metric_name in metric_names:
            group_by_model[model_name].append(pearsons[dataset_name][model_name][metric_name])

for i in range(len(model_names)):
    if i + 1 >= len(metric_names):
        break

    for j in range(i + 1, len(model_names)):
        model_name1 = model_names[i]
        model_name2 = model_names[j]

        if average(group_by_model[model_name1]) > average(group_by_model[model_name2]):
            model_name1, model_name2 = model_name2, model_name1

        significance_result = test_significance(group_by_model[model_name1], group_by_model[model_name2])

        print('{0} vs {1}'.format(model_name1, model_name2))
        print(dumps(significance_result, indent=4))

print('-' * 30)
print('Group by metric')
print('-' * 30)
group_by_metric = {metric_name: [] for metric_name in metric_names}
for dataset_name in dataset_names:
    for model_name in model_names:
        for metric_name in metric_names:
            group_by_metric[metric_name].append(pearsons[dataset_name][model_name][metric_name])

for i in range(len(metric_names)):
    if i + 1 >= len(metric_names):
        break

    for j in range(i + 1, len(metric_names)):
        metric_name1 = metric_names[i]
        metric_name2 = metric_names[j]

        if average(group_by_metric[metric_name1]) > average(group_by_metric[metric_name2]):
            model_name1, model_name2 = metric_name2, metric_name1

        significance_result = test_significance(group_by_metric[metric_name1], group_by_metric[metric_name2])

        print('{0} vs {1}'.format(metric_name1, metric_name2))
        print(dumps(significance_result, indent=4))


print(dumps(pearsons, indent=4))