import os, sys
sys.path.append('C:/git/STS/Optimizing/')
from corpora_modification_scripts.Util import get_unique_dataset_words

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'r', encoding='utf-8') as store_file:
    lines = store_file.readlines()

vector_words = [word for word in get_unique_dataset_words()]
for i in range(1, len(vector_words)):
    lines[i] = vector_words[i][0] + lines[i]

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'w', encoding='utf-8') as store_file:
    store_file.writelines(lines)
    store_file.flush()
    os.fsync(store_file)
