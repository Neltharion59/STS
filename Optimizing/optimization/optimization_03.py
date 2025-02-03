# Runnable script performing renewed type of optimization.

import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

import math
import json
import os
import sys
from datetime import datetime

from sklearn.exceptions import ConvergenceWarning
from sklearn.utils._testing import ignore_warnings
from Hive import Hive
from playsound import playsound

from complex_similarity_methods.dataset_fragmentation import FragmentedDatasetCV, FragmentedDatasetSuper
from dataset_modification_scripts.dataset_pool import dataset_pool
from evaluation.evaluate_regression_metrics import pearson
from model_management.persistent_id_generator import PersistentIdGenerator
from model_management.sts_model_pool import model_types
from util.file_handling import write, exists, read
from util.math import average


path_to_optimizer_run_record_folder = os.path.join(root_path, 'resources/optimizer_runs/')
dataset_file_pattern = 'resources/split_datasets/split_dataset_{0}_{1}_sk.json'

# Configuration - parameters of optimization
cross_validation_fold_count = 10
fitness_metric = {
    'name': 'pearson',
    'method': pearson
}
bee_count = 1
iteration_cap = 1

# Optimization run record object that will be persisted.
algorithm_run = {
    'run_id': PersistentIdGenerator('optimizer_run').next_id(),
    'config': {
        'CV_fold_count': cross_validation_fold_count,
        'fitness_metric': fitness_metric['name'],
        'optimizer': {
            'name': 'ABC',
            'config': {
                'bee_count': bee_count,
                'iteration_cap': iteration_cap
            }
        }
    },
    'main': {}
}

# Dataset-specific
split_dataset_master = None
sorted_method_group_names = None
method_count = None
method_param_counts = None

# Dataset&Model-specific
sorted_arg_names = None
arg_possibility_counts = None
best_model = None
model_id_generator = PersistentIdGenerator('model_persistence')


# Persistence-related util function. If record of run with this id already exists, let's load the existing object
# and use it instead of a new one.
# Params: int
# Return: None
def load_optimizer_run(run_id):
    try:
        txt_dump = read('{}optimizer_run_{}.txt'.format(path_to_optimizer_run_record_folder, run_id))
        print('--- OLD --- Run with id {} exists. Let\'s continue where we dropped off'.format(run_id))
        global algorithm_run
        algorithm_run = json.loads(txt_dump)
    except FileNotFoundError:
        print('--- NEW --- Run with id {} does not exist. Let\'s start a new one'.format(run_id))


# Persistence - related util function. Persist the optimizer run record object.
# Params:
# Return: None
def persist_optimizer_run():
    txt_dump = json.dumps(algorithm_run, indent=4)
    write('{}optimizer_run_{}.txt'.format(path_to_optimizer_run_record_folder, algorithm_run['run_id']), txt_dump)


# FITNESS FUNCTION
# Beehive looks for minimum. Make this so that lowest value of this function means the best solution.
# Params: list<float>
# Return: float
@ignore_warnings(category=ConvergenceWarning)
def solution_evaluator(vector):
    global optimizer_iteration_counter, best_model

    optimizer_iteration_counter = optimizer_iteration_counter + 1

    # Print the iteration progress of algorithm. Note that we do not want to modify the ABC algorithm library(Hive),
    # so we simply estimate the iteration based on how many times fitness function was called. The estimation
    # is a little inacurate, so we often get more iterations than we estimated there would be.
    if optimizer_iteration_counter % 2 == 0:
        temp = optimizer_iteration_counter // 2

        if temp % bee_count == 1:
            global iteration_start, iteration_end
            iteration_end = datetime.now()
            print('\tIteration (estimate) {}/{}, took {}. Best fitness: {}'.format(temp // bee_count + 1, iteration_cap, iteration_end - iteration_start, best_model['fitness']))
            iteration_start = iteration_end

    # All values are float and are supposed to be array indeces, so let's turn them to ints.
    temp_vector = list(map(lambda x: int(x), vector))
    param_dict = {}

    # Hyperparameters of model.
    for i in range(len(sorted_arg_names)):
        param_dict[sorted_arg_names[i]] = model_type['args'][sorted_arg_names[i]][temp_vector[i]]

    # Features to be fed to model
    inputs = []
    temp_vector_starting_index = len(sorted_arg_names)
    for i in range(method_count):
        if temp_vector[temp_vector_starting_index + i] < method_param_counts[i]:
            inputs.append({
                'method_name': sorted_method_group_names[i],
                'args': split_dataset_master.Train.features[sorted_method_group_names[i]][temp_vector[temp_vector_starting_index + i]]['args'],
                'values': split_dataset_master.Train.features[sorted_method_group_names[i]][temp_vector[temp_vector_starting_index + i]]['values']
            })

    # Less than two features wouldn't make a very good model.
    if len(inputs) < 2:
        return 2

    # Prepare data for model - split to folds of CV
    dataset_fragments = FragmentedDatasetCV(inputs, split_dataset_master.Train.labels, cross_validation_fold_count)
    metric_values_test = []
    models = []
    # Perform CV
    for k in range(len(dataset_fragments.folds)):
        # Prepare train and test set for this fold
        model_data = dataset_fragments.produce_split_dataset(k).produce_sklearn_ready_data()

        # Prepare and train the model
        model = model_type['model'](**param_dict)
        model.fit(model_data.train.features, model_data.train.labels)
        # Evaluate the model
        metric_value = fitness_metric['method'](model_data.test.labels, model.predict(model_data.test.features))
        # If model is valid, let's add to list of CV-trained models
        if not math.isnan(metric_value):
            models.append(model)
            metric_values_test.append(metric_value)

    # If no models is valid, we have bad configuration
    if len(metric_values_test) == 0:
        print('\tModel with NaN metric for all CV folds')
        return 2

    # Determine the metric and the model best representing the configuration
    metric_test_avg = average(metric_values_test)

    # Calculating final fitness is simple
    fitness = 1 - metric_test_avg

    # If this model is the current best, let's save it
    if best_model is None or fitness < best_model['fitness']:
        best_model = {
            'inputs': [{'method_name': x['method_name'], 'args': x['args']} for x in inputs],
            'fitness': fitness,
            'pearson': metric_test_avg,
            'hyperparams': param_dict
        }

    return fitness


# Function wrapping running single optimization.
# Params:
# Return: None
def run_optimization():
    # Create optimizer model
    model = Hive.BeeHive(
        lower=[0] * (len(arg_possibility_counts) + method_count),
        upper=list(map(lambda x: x - 1, arg_possibility_counts)) + list(map(lambda x: 2 * x - 1, method_param_counts)),
        fun=solution_evaluator,
        numb_bees=bee_count,
        max_itrs=iteration_cap
    )

    # Run the optimization
    optimizer_start = datetime.now()
    cost = model.run()
    optimizer_end = datetime.now()
    print('Optimization took: {}'.format(optimizer_end - optimizer_start))

    print("Best model:\n\tFitness: {}".format(best_model['fitness']))

    if 'models' not in algorithm_run['main'][key][dataset.name]:
        algorithm_run['main'][key][dataset.name]['models'] = {}

    # Persist the model
    global model_type
    best_model['type'] = model_type['name']

    # Record the model in the optimizer run record object.
    algorithm_run['main'][key][dataset.name]['models'][model_type['name']]['best_model'] = best_model
    algorithm_run['main'][key][dataset.name]['models'][model_type['name']]['fitness_history'] = cost

# Try to load the optimizer run (if there is already a run with this ID)
load_optimizer_run(algorithm_run['run_id'])

dataset_counter = 1
dataset_counter_max = len(list(dataset_pool.keys())) * len(dataset_pool[list(dataset_pool.keys())[0]])

model_in_dataset_counter_max = len(model_types)

total_counter = 1
total_counter_max = dataset_counter_max * model_in_dataset_counter_max

global_start = datetime.now()

split_dataset_file_pattern = 'resources/split_datasets/split_dataset_{0}_{1}_sk.json'
try:
    # For each dataset version (raw vs. lemma)
    for key in dataset_pool:

        if key not in algorithm_run['main']:
            algorithm_run['main'][key] = {}
        # For each dataset
        for dataset in dataset_pool[key]:
            if dataset.name not in algorithm_run['main'][key]:
                algorithm_run['main'][key][dataset.name] = {}

            split_dataset_master_json = json.loads(read(split_dataset_file_pattern.format(dataset.name, key)))

            split_dataset_master = FragmentedDatasetSuper()
            split_dataset_master.from_json(split_dataset_master_json)

            model_in_dataset_counter = 1
            # For each model type
            for model_type in model_types:
                # Notify of progress
                print('DATASET {}: {}/{} | MODEL {}: {}/{} | TOTAL: {}/{} {}%'.format(

                    dataset.name, dataset_counter, dataset_counter_max,
                    model_type['name'], model_in_dataset_counter, model_in_dataset_counter_max,
                    total_counter, total_counter_max, round(total_counter / total_counter_max, ndigits=4) * 100
                ))

                if 'models' not in algorithm_run['main'][key][dataset.name]:
                    algorithm_run['main'][key][dataset.name]['models'] = {}
                # If this model type has already been trained for this dataset in this run, let's skip,
                # otherwise it is time to optimize
                if model_type['name'] not in algorithm_run['main'][key][dataset.name]['models']:
                    print('DOES NOT EXIST - TRAINING')
                    algorithm_run['main'][key][dataset.name]['models'][model_type['name']] = {}

                    # Load available values for this dataset
                    dataset_file_path = dataset_file_pattern.format(dataset.name, key)
                    persisted_values = json.loads(read(dataset_file_path))

                    persisted_methods_temp = persisted_values['Train']['features']
                    gold_values_temp = persisted_values['Train']['labels']

                    # Prepare helpful values for more concise programming later
                    sorted_method_group_names = sorted(persisted_methods_temp.keys())
                    method_count = len(sorted_method_group_names)

                    method_param_counts = [len(persisted_methods_temp[sorted_method_group_names[i]])
                                           for i in range(method_count)]

                    sorted_arg_names = sorted(model_type['args'].keys())
                    arg_possibility_counts = list(map(lambda x: len(model_type['args'][x]), sorted_arg_names))

                    if 'available_methods' not in algorithm_run['main'][key][dataset.name]:

                        possibilities = {method_name: [config['args'] for config in persisted_methods_temp[method_name]] for method_name in sorted_method_group_names}
                        algorithm_run['main'][key][dataset.name]['available_methods'] = possibilities

                    # Prepare for optimization
                    best_model = None
                    optimizer_iteration_counter = 0
                    iteration_start = datetime.now()
                    iteration_end = None
                    # Run the optimization
                    run_optimization()
                    # Persist the optimization run record
                    persist_optimizer_run()

                else:
                    print('EXISTS - SKIPPING')

                model_in_dataset_counter = model_in_dataset_counter + 1
                total_counter = total_counter + 1

            dataset_counter = dataset_counter + 1

    # Play the sound - useful notification, as someone usually waits for hours until this is over.
    playsound(os.path.join(root_path, 'sounds/victory.mp3'))
    print('ENTIRE ALGORITHM TOOK {}'.format(datetime.now() - global_start))

except:
    # Play the sound - useful notification, as someone usually waits for hours until this is over.
    playsound(os.path.join(root_path, 'sounds/wrong.mp3'))
    print('ENTIRE ALGORITHM TOOK {}'.format(datetime.now() - global_start))

    # Raise the alert again
    raise sys.exc_info()[0]
