import sys
sys.path.append('C:/git/STS/Optimizing/')
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words
from util.get_wiki_article import get_wiki_article, tf_idf
from os import fsync

vector_file_path = '../resources/vector/esa_full.txt'
progress_file_path = '../resources/temp/progress_esa_vectors_full.txt'

vector_words = [word for word in get_unique_dataset_words()]
vector_words_count = len(vector_words)

try:
    with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
        starting_word = int(progress_file.read())
except FileNotFoundError:
    starting_word = 0

records = []
for i in range(starting_word, len(vector_words)):
    word = vector_words[i]

    wiki_words = get_wiki_article(word)
    wiki_words_tf_idf = [str(round(tf_idf(wiki_word, wiki_words), 2)) for wiki_word in wiki_words]
    values = ','.join(wiki_words_tf_idf)
    records.append(f'{word} {values}')

    if i > 0 and i % 10 == 0:
        print(f'Processing {i}/{vector_words_count}. {i/vector_words_count * 100}%')

        with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
            progress_file.write(str(i))
            progress_file.flush()
            fsync(progress_file)

        with open(vector_file_path, 'a+', encoding='utf-8') as vector_file:
            vector_file.write('\n'.join(records))
            vector_file.flush()
            fsync(vector_file)

        records = []

if len(records) > 0:
    with open(vector_file_path, 'a+', encoding='utf-8') as vector_file:
        vector_file.write('\n'.join(records))
        vector_file.flush()
        fsync(vector_file)

with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
    progress_file.write(str(vector_words_count))
    progress_file.flush()
    fsync(progress_file)
