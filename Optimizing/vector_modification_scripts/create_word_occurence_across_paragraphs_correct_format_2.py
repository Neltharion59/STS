import os

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'r', encoding='utf-8') as store_file:
    lines = store_file.readlines()

vector_words = [word for word in get_unique_dataset_words()]
for word in vector_words:
    print(word)
exit(0)

for line in lines:
    print(line)
exit(0)

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'w', encoding='utf-8') as store_file:
    store_file.writelines(lines)
    store_file.flush()
    os.fsync(store_file)
