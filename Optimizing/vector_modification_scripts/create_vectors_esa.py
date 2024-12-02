import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words
from util.get_wiki_article import get_wiki_article, tf_idf
from util.file_handling import read, write
from os import fsync
from json import dumps, loads

vector_file_path = './resources/vector/esa_v1_full.txt'

vector_words = [word for word in get_unique_dataset_words()]
vector_words_count = len(vector_words)

try:
    records = loads(read(vector_file_path))
except FileNotFoundError:
    records = {}

i = 0
for word in vector_words:
    i = i + 1

    if word in records:
        continue

    wiki_words = get_wiki_article(word)
    wiki_words_tf_idf = [str(round(tf_idf(wiki_word, wiki_words), 2)) for wiki_word in wiki_words]
    values = ','.join(wiki_words_tf_idf)
    records[word] = values

    if i % 20 == 0:
        print(f'Processing {i}/{vector_words_count}. {i/vector_words_count * 100}%')
        write(vector_file_path, dumps(records))

write(vector_file_path, dumps(records))

