import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import loads

from util.file_handling import read
from evaluation.evaluate_regression_metrics import pearson, spearman
from dataset_modification_scripts.dataset_pool import dataset_pool
from dataset_modification_scripts.dataset_wrapper import gold_standard_name

prediction_object = {
    'stsbenchmark': [x['similarity_score'] for x in loads(read('./resources/stsbenchmark_sk_results_NLP.json'))],
    'sick': [x['similarity_score'] for x in loads(read('./resources/sick_sk_results_NLP.json'))]
}

for dataset in dataset_pool['raw']:
    labels = dataset.load_values()[gold_standard_name][0]['values']
    predictions = prediction_object[dataset.name]
    correlation_pearson = pearson(labels, predictions)
    correlation_spearman = spearman(labels, predictions)
    print('{0}: Pearson - {1}, Spearman- {2}', dataset.name, correlation_pearson, correlation_spearman)
