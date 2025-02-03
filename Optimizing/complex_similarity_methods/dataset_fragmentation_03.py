# Library-like script providing wrapper class for datasets

from random import shuffle

import numpy as np


# Cute little class that split dataset values to 'k' stratified folds (as in cross-validation).
class FragmentedDatasetCV:
    # Constructor
    # Params: list<dict<str, any>>, list<float>, int
    # Return: FragmentedDatasetCV
    def __init__(self):
        self.k_fold = 0
        self.fold_indices = []
        self.fold_labels = []
        self.fold_features = {}

    def from_full_dataset(
        self,
        inputs,
        gold_values,
        k_fold
    ):
        # Split to classes for stratification - prepare variables.
        class_grouped_indices = []
        class_count = 5
        for i in range(class_count):
            class_grouped_indices.append([])
        # Split to classes for stratification - perform the split.
        for i in range(len(gold_values)):
            index = min(4, int(gold_values[i] * class_count))
            class_grouped_indices[index].append(i)
        # If there are empty classes, we may ignore them.
        for i in reversed(range(class_count)):
            if len(class_grouped_indices[i]) == 0:
                del class_grouped_indices[i]
                class_count = class_count - 1
        # Shuffle each class randomly.
        for i in range(class_count):
            temp = class_grouped_indices[i]
            shuffle(temp)
            class_grouped_indices[i] = temp

        # Split to dataset fragments - prepare variables.
        fold_indices = []
        for k in range(k_fold):
            fold_indices.append([])
        # Split to dataset fragments - perform the split.
        for i in range(class_count):
            # Calculate single fold size.
            train_size = len(class_grouped_indices[i])
            batch_size = int(train_size / k_fold)
            index_range = (0, batch_size)
            # Create the folds.
            for k in range(k_fold):
                fold_indices[k] = fold_indices[k] + class_grouped_indices[i][index_range[0]:index_range[1]]
                index_range = (index_range[1], train_size if k == (k_fold - 1) else (index_range[1] + batch_size))

        self.k_fold =k_fold
        self.fold_indices = fold_indices
        self.fold_labels = [[gold_values[index_j] for index_j in fold_indices[fold_i]] for fold_i in range(len(fold_indices))]

        fold_features = {}
        for method_name in inputs:
            fold_features[method_name] = []

            for i in range(len(inputs[method_name])):
                fold_features[method_name].append({
                    'args': inputs[method_name][i]['args'],
                    'values': [[inputs[method_name][i]['values'][index_j] for index_j in fold_indices[fold_i]] for fold_i in range(len(fold_indices))]
                })
        self.fold_features = fold_features

    def produce_subset(self, inputs):
        features = []

        for i in range(self.k_fold):
            fold_features = []

            for x in inputs:
                method_name = x['method_name']
                arg_index = x['arg_index']
                method_variations = self.fold_features[method_name]
                values = method_variations[arg_index]['values']
                value = values[i]
                fold_features.append(value)

            features.append(fold_features)

        transposed = [[list(row) for row in zip(*features[i])] for i in range(self.k_fold)]

        subset = FragmentedDatasetCVSubset()
        subset.from_data(self.fold_labels, transposed)

        return subset

    # Produce dataset where n-th fold is the testing set.
    # Params: int
    # Return: SingleFoldDatasetFragment


class FragmentedDatasetCVSubset:
    def __init__(self):
        self.fold_count = 0
        self.fold_labels = []
        self.fold_features = []

    def from_data(self, fold_labels, fold_features):
        self.fold_count = len(fold_labels)
        self.fold_labels = fold_labels
        self.fold_features = fold_features

    def produce_split_dataset(self, fold_index):
        # Prepare test fragment.
        test_fragment = SingleDatasetFragment(self.fold_labels[fold_index], self.fold_features[fold_index])
        # Prepare train fragment.
        train_fragment = SingleDatasetFragment([], [])
        for k in range(self.fold_count):
            # This fold is test fragment.
            if k == fold_index:
                continue
            # Append to train fragment.
            train_fragment.labels = train_fragment.labels + self.fold_labels[k]
            train_fragment.features = train_fragment.features + self.fold_features[k]
        # Wrap train and test in a class.
        return SingleFoldDatasetFragment(train_fragment, test_fragment)


# Cute little class that conveniently wraps a dataset with simple access to features and labels.
class SingleDatasetFragment:
    # Constructor
    # Params: list<float>, list<list<float>>
    # Return: SingleDatasetFragment
    def __init__(self, labels, features):
        self.labels = labels
        self.features = features


# Cure little class that conveniently wraps dataset split to train and test subset. To us, it is a single fold of CV.
class SingleFoldDatasetFragment:
    # Constructor
    # Params: SingleDatasetFragment, SingleDatasetFragment
    # Return: SingleFoldDatasetFragment
    def __init__(self, train_fragment, test_fragment):
        self.train = train_fragment
        self.test = test_fragment

    # Puts data into form required by sklearn models.
    # Params:
    # Return: SingleFoldDatasetFragment
    def produce_sklearn_ready_data(self):
        # Prepare train subset.
        skl_ready_labels = np.array(self.train.labels)
        skl_ready_features = np.array(self.train.features)
        print("Shape of array:", self.train.features.shape)
        skl_ready_train = SingleDatasetFragment(skl_ready_labels, skl_ready_features)
        # Prepare test subset.
        skl_ready_labels = np.array(self.test.labels)
        skl_ready_features = np.array(self.test.features)
        skl_ready_test = SingleDatasetFragment(skl_ready_labels, skl_ready_features)
        # Wrap in class
        return SingleFoldDatasetFragment(skl_ready_train, skl_ready_test)


# Cute little class that wraps dataset split to validation subset and CV-ready subset for training
# (and performs the split).
class FragmentedDatasetSuper:
    def __init__(self):
        self.Train = None
        self.Validation = None
        pass

    # Constructor
    # Params: dict<str, dict<str, any>>, list<float>, DatasetSplitRatio
    # Return: FragmentedDatasetSuper
    def from_full_dataset(self, available_methods, gold_values, split_ratio):
        dataset_size = len(available_methods[list(available_methods.keys())[0]][0]['values'])
        # Make sure that the data is consistent it terms of size
        for method_name in available_methods:
            for method_config in available_methods[method_name]:
                if len(method_config['values']) != dataset_size:
                    raise ValueError('Value count inconsistent')
        if len(gold_values) != dataset_size:
            raise ValueError('Gold value count inconsistent')
        # On which index the dataset should be split
        split_index = int(split_ratio.train_ratio * dataset_size)
        # Shuffle the data (it is easier to shuffle indices of rows than to rows themselves)
        indices = list(range(dataset_size))
        shuffle(indices)
        # Prepare labels.
        reordered_gold_train, reordered_gold_valid = [gold_values[i] for i in indices[:split_index]], [gold_values[i] for i in indices[split_index:]]
        # Prepare features.
        reordered_train, reordered_valid = {}, {}
        for method_name in available_methods:
            reordered_train[method_name], reordered_valid[method_name] = [], []
            for method_config in available_methods[method_name]:
                reordered_train[method_name].append({
                    'args': method_config['args'],
                    'values': [method_config['values'][i] for i in indices[:split_index]]
                })
                reordered_valid[method_name].append({
                    'args': method_config['args'],
                    'values': [method_config['values'][i] for i in indices[split_index:]]
                })
        # Make sure we did not mess it on train subset.
        for method_name in reordered_train:
            for method_config in reordered_train[method_name]:
                if len(method_config['values']) != split_index:
                    raise ValueError('Train Value count inconsistent')
        if len(reordered_gold_train) != split_index:
            raise ValueError('Train Gold value count inconsistent')
        # Make sure we did not mess it on validation subset.
        for method_name in reordered_valid:
            for method_config in reordered_valid[method_name]:
                if len(method_config['values']) != dataset_size - split_index:
                    raise ValueError('Validation Value count inconsistent')
        if len(reordered_gold_valid) != dataset_size - split_index:
            raise ValueError('Validation Gold value count inconsistent')
        # Wrap in classes.
        self.Train = SingleDatasetFragment(reordered_gold_train, reordered_train)
        self.Validation = SingleDatasetFragment(reordered_gold_valid, reordered_valid)

    def from_json(self, json_split):
        self.Train = SingleDatasetFragment(json_split['Train']['labels'], json_split['Train']['features'])
        self.Validation = SingleDatasetFragment(json_split['Validate']['labels'], json_split['Validate']['features'])
