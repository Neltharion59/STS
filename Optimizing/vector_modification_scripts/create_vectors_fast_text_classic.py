import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from json import dumps
from util.file_handling import read, write
from corpora_modification_scripts.Util import get_unique_dataset_words

unique_dataset_words = get_unique_dataset_words()
new_vectors = {}

with open(os.path.join(root_path, './resources/vector/cc.sk.300.vec'), 'r', encoding='utf-8', newline='\n', errors='ignore') as vector_file:
    first = True
    for line in vector_file:
        if first:
            first = False
            continue

        tokens = line.replace('\n', '').split(' ')
        word = tokens[0]

        if word in unique_dataset_words:
            vector = [float(token) for token in tokens[1:]]
            new_vectors[word] = vector

write(os.path.join(root_path, './resources/vector/fast_text_classic.json'), dumps(new_vectors))
