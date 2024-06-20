import sys
import os
conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

from os import listdir, fsync
from os.path import isfile, join
from functools import reduce
import re
import mysql.connector
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words


#window_size = 10
window_radius = 5
frame_size = window_radius * 2 + 1

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sts_data",
  charset='utf8',
  use_unicode=True
)

mycursor = mydb.cursor()

vector_words = get_unique_dataset_words()


def is_vector_word(word):
    return word in vector_words


def is_feature_word(word):
    pass


def save_word(id_row, id_col, inc):
    sql_save = f"INSERT INTO cell_hal (id_row, id_col, value) VALUES({id_row}, {id_col}, {inc}) ON DUPLICATE KEY UPDATE cell_hal.value = cell_hal.value + {inc};"
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


corpora_directory_path = './../resources/corpora/processed/'

corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = [x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)]
corpus_progress_track_file_name_pattern = "progress_vector_hal_construction_oscarsk_{}"

for input_corpus_file in input_corpus_files:
    corpus_file_path = join(corpora_directory_path, input_corpus_file)
    dataset_part_id = corpus_file_path.replace('oscarsk_meta_part_', '').replace('_sk_lemma.jsonl', '').replace(corpora_directory_path, '')
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
            for i in range(len(tokens)):
                if not is_vector_word(tokens[i]):
                    continue

                row_id = total_words[tokens[i]]
                if row_id not in buffer:
                    buffer[row_id] = {}
                for j in range(max(0, i - window_radius), min(len(tokens), i + window_radius)):
                    if i == j:
                        continue

                    if not is_feature_word(tokens[j]):
                        continue

                    col_id = total_words[tokens[j]]
                    increment = frame_size - abs(i - j)
                    if col_id not in buffer[row_id]:
                        buffer[row_id][col_id] = increment
                    else:
                        buffer[row_id][col_id] = buffer[row_id][col_id] + increment

            if current_line % 10 == 0:
                print('---saving---')
                item_ctn = reduce(lambda a, b: a + b, [len(buffer[key].keys()) for key in buffer])
                current_item = 0

                mycursor.close()
                mycursor = mydb.cursor()

                for row_id in buffer:
                    for col_id in buffer[row_id]:
                        current_item = current_item + 1
                        save_word(row_id, col_id, buffer[row_id][col_id])

                        if current_item % 10000 == 0:
                            print(f'{input_corpus_file} Saving buffer item {str(current_item)}/{str(item_ctn)} - {str(current_item / item_ctn * 100)}%')

                buffer = {}
                print('---commiting---')
                mydb.commit()
                with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
                    progress_file.write(str(current_line))
                    progress_file.flush()
                    fsync(progress_file)

        print('---saving---')
        item_ctn = reduce(lambda a, b: a + b, [len(buffer[key].keys()) for key in buffer])
        current_item = 0

        mycursor.close()
        mycursor = mydb.cursor()

        for row_id in buffer:
            for col_id in buffer[row_id]:
                current_item = current_item + 1
                save_word(row_id, col_id, buffer[row_id][col_id])

                if current_item % 10000 == 0:
                    print(f'{input_corpus_file} Saving buffer item {str(current_item)}/{str(item_ctn)} - {str(current_item / item_ctn * 100)}%')

        buffer = {}
        print('---commiting---')
        mydb.commit()
        with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
            progress_file.write(str(current_line))
            progress_file.flush()
            fsync(progress_file)

    mycursor.close()

mydb.close()
