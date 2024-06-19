import os
import csv

input_directory = './../resources/datasets/raw'
input_files = ['sts-dev.csv', 'sts-test.csv', 'sts-train.csv']
target_file = './../resources/datasets/sts_processed/stsbenchmark_en.txt'

merged_dataset_rows = []

for input_file in input_files:
    input_file_path = os.path.join(input_directory, input_file)

    with open(input_file_path, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')

        for row in spamreader:
            merged_dataset_rows.append('\t'.join(row[4:7]))

merged_dataset = '\n'.join(merged_dataset_rows)

with open(target_file, encoding='utf-8', mode='w') as txtfile:
    txtfile.write(merged_dataset)
