import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import loads, dumps

from util.file_handling import read, write
from model_management.persistent_id_generator import PersistentIdGenerator

new_id = PersistentIdGenerator('optimizer_run').next_id()
run_paths = {
    'raw': './resources/optimizer_runs_final/optimizer_run_raw.json',
    'lemma': './resources/optimizer_runs_final/optimizer_run_lemma.json'
}
for key in run_paths:
    run_paths[key] = os.path.join(root_path, run_paths[key])

merged = {
    'run_id': new_id,
    'config': {
        'CV_fold_count': 10,
        'fitness_metric': 'pearson',
        'optimizer': {
            'name': 'ABC',
            'config': {
                'bee_count': 50,
                'iteration_cap': 30
            }
        }
    },
    'main': { dataset_version: {} for dataset_version in run_paths}
}
for dataset_version in run_paths:
    temp = loads(read(run_paths[dataset_version]))
    for dataset_name in temp['main'][dataset_version]:
        merged['main'][dataset_version][dataset_name] = temp['main'][dataset_version][dataset_name]

merged_json = dumps(merged ,indent=4)

output_folder = os.path.join(root_path, './resources/optimizer_runs_final/optimizer_run_final.json')
write(output_folder, merged_json)