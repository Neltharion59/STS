import re
from os import listdir, fsync
from os.path import isfile, join

corpora_directory_path = './../resources/corpora/processed/'
corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
target_file_path = '../resources/corpora_line_count.txt'

corpus_file_paths = [x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)]

acc = 0
for corpus_file_path in corpus_file_paths:
    with open(join(corpora_directory_path, corpus_file_path), 'r', encoding='utf-8') as corpus_file:
        acc = acc + len(list(corpus_file.readlines()))

    with open(target_file_path, 'w+', encoding='utf-8') as target_file:
        target_file.write(str(acc))
        target_file.flush()
        fsync(target_file)


