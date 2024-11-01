vector_file_path = '../resources/vector/lsa_full_{}_1000.txt'
batch_ids = list(range(0, 18))

paragraphs_occured_in_counts = []

for batch_id in batch_ids:
    current_vector_file_path = vector_file_path.format(batch_id)

    with open(current_vector_file_path, 'r', encoding='utf-8') as current_vector_file:
        lines = current_vector_file.readlines()

    print(f'Loaded {batch_id}/17')
    i = 0
    for line in lines:
        tokens = line.split('\t')
        word = tokens[0]
        paragraphs_occured_in_count = len([x for x in tokens[1].split(',') if x != '0'])
        paragraphs_occured_in_counts.append(f'{word} {paragraphs_occured_in_count}')

        if i % 10 == 0:
            print(f'Batch {batch_id}. Line {i}')
            print(paragraphs_occured_in_counts)

        i = i + 1

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'w+', encoding='utf-8') as store_file:
    store_file.writelines(paragraphs_occured_in_counts)


