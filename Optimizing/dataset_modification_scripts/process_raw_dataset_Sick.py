import os

input_file = './../resources/datasets/raw/sick.txt'
target_file = './../resources/datasets/sts_processed/sick_en.txt'

modified_dataset_rows = []
columns = [4, 1, 2]

with open(input_file, encoding='utf-8') as file:
    first_row = True
    for row in file:
        if first_row:
            first_row = False
            continue

        split_row = row.split('\t')
        relevant_data = [split_row[column] for column in columns]
        modified_dataset_rows.append('\t'.join(relevant_data))

merged_dataset = '\n'.join(modified_dataset_rows)

with open(target_file, encoding='utf-8', mode='w') as txtfile:
    txtfile.write(merged_dataset)
