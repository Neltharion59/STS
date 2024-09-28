import sys
import os
conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from os import listdir, fsync
from os.path import isfile, join
from functools import reduce
import re
import mysql.connector
from corpora_modification_scripts.Util import split_to_words

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sts_data",
  charset='utf8',
  use_unicode=True
)

mycursor = mydb.cursor()

corpora_directory_path = './../resources/corpora/processed/'


def save_paragraph(file_id):
    sql_save = f"INSERT INTO paragraph (id_file) VALUES({file_id});"
    mycursor.execute(sql_save)
    return mycursor.lastrowid


def save_word_occurence(id_word, id_paragraph, value):
    sql_save = f"INSERT INTO cell_occurence (id_word, id_par, value) VALUES({id_word}, {id_paragraph}, {value});"
    mycursor.execute(sql_save)
    return sql_save


def get_all_words():
    sql_get = f"SELECT word.text, word.id FROM word;"
    mycursor.execute(sql_get)
    myresult = mycursor.fetchall()

    result = {}
    for mr in myresult:
        result[mr[0]] = mr[1]
    return result


def get_corpus_file_id(corpus_file_name):
    return corpus_file_name.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')


def persist_collected_data(buffer, is_last=False):
    if len(buffer.keys()) == 0:
        return

    #print('---saving---')
    #item_ctn = reduce(lambda a, b: a + b, [len(buffer[key].keys()) for key in buffer])
    #current_item = 0

    for par_id in buffer:
        for token_id in buffer[par_id]:
            #current_item = current_item + 1
            save_word_occurence(token_id, par_id, buffer[par_id][token_id])

            #if current_item % 1000 == 0:
            #    print(f'{input_corpus_file} Saving buffer item {str(current_item)}/{str(item_ctn)} - {str(current_item / item_ctn * 100)}%')

    #print('---commiting---')
    mydb.commit()
    with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
        progress_file.write('-1' if is_last else str(current_line))
        progress_file.flush()
        fsync(progress_file)


corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = sorted([x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)], key=lambda x: int(get_corpus_file_id(x)))
corpus_progress_track_file_name_pattern = "progress_vector_lsa_construction_oscarsk_{}"

for input_corpus_file in input_corpus_files:
    corpus_file_path = join(corpora_directory_path, input_corpus_file)
    dataset_part_id = get_corpus_file_id(corpus_file_path)
    progress_file_path = './../resources/temp/' + corpus_progress_track_file_name_pattern.format(dataset_part_id) + '.txt'

    last_processed_line = 0
    try:
        with open(progress_file_path, 'r', encoding='utf-8') as progress_file:
            last_processed_line = int(progress_file.read())
    except FileNotFoundError:
        last_processed_line = 0

    if last_processed_line == -1:
        continue

    current_line = 0
    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        total_lines = len(corpus_file.readlines())

    mycursor = mydb.cursor()
    total_words = get_all_words()
    buffer = {}

    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        for line in corpus_file:
            current_line = current_line + 1

            if current_line <= last_processed_line:
                continue
            print(f'{input_corpus_file} Processing line {str(current_line)}/{str(total_lines)} - {str(current_line/total_lines*100)}%')

            tokens = split_to_words(line)
            tokens = [token for token in tokens if token in total_words]

            par_id = save_paragraph(dataset_part_id)
            buffer[par_id] = {}

            for token in tokens:
                token_id = total_words[token]
                if token_id not in buffer[par_id]:
                    buffer[par_id][token_id] = 1
                else:
                    buffer[par_id][token_id] = buffer[par_id][token_id] + 1

            mycursor.close()
            mycursor = mydb.cursor()
            persist_collected_data(buffer)
            buffer = {}

        mycursor.close()
        mycursor = mydb.cursor()
        persist_collected_data(buffer, True)
        buffer = {}

    mycursor.close()

mydb.close()
