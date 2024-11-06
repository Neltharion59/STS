import os

vector_file_path = '../resources/vector/lsa_full_{}_1000.txt'
progress_file_path = '../resources/temp/progress_word_occurence_across_paragraphs.txt'

try:
    with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
        start_batch = int(progress_file.read())
except FileNotFoundError:
    start_batch = 0
batch_ids = list(range(start_batch, 18))

for batch_id in batch_ids:
    paragraphs_occured_in_counts = []

    current_vector_file_path = vector_file_path.format(batch_id)

    with open(current_vector_file_path, 'r', encoding='utf-8') as current_vector_file:
        lines = current_vector_file.readlines()

    print(f'Loaded {batch_id}/17')
    i = 0
    for line in lines:
        tokens = line.split('\t')
        word = tokens[0]
        paragraphs_occured_in_count = len([x for x in tokens[1].split(',') if x != '0'])
        new_record = f'{word} {paragraphs_occured_in_count}'
        paragraphs_occured_in_counts.append(new_record)

        print(f'Batch {batch_id}. Line {i}. {new_record}')
        i = i + 1

    with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'a+', encoding='utf-8') as store_file:
        store_file.writelines(paragraphs_occured_in_counts)
        store_file.flush()
        os.fsync(store_file)

    with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
        progress_file.write(str(batch_id))
        progress_file.flush()
        os.fsync(progress_file)

    paragraphs_occured_in_counts = []
