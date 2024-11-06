output_path_pattern = '../resources/basic_values/{0}/pmi_{1}.txt'

dataset_version = ['raw', 'lemma']
dataset_names = []
dataset_texts = {}

config_options = {
    'match_strategy': ['each', 'pos'],
    'merge_strategy': ['avg', 'min', 'max']
}+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++6























































































all_config_perms = []


def pmi(text1, text2, configuration):
    pass


records = []
for dataset_version in dataset_versions:
    for dataset_name in dataset_names:
        for config in all_config_perms:
            for words1, words2 in dataset_texts[dataset_version][dataset_name]:
                record_pmi = pmi(words1, words2, config)
                records.append(record_pmi)

