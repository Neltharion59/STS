from os import listdir, fsync
from os.path import isfile, join
import re
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sts_data",
  charset='utf8',
  use_unicode=True
)

mycursor = mydb.cursor()


def save_word(word):
    sql_save = f"INSERT INTO word (word.text) VALUES ('{word}');"
    mycursor.execute(sql_save)


def get_all_words():
    sql_get = f"SELECT word.text FROM word;"
    mycursor.execute(sql_get)
    myresult = mycursor.fetchall()

    result = {}
    for mr in myresult:
        result[mr[0]] = 0
    return result


corpora_directory_path = './../resources/corpora/processed/'

corpus_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+_sk_lemma.jsonl")
input_corpus_files = [x for x in listdir(corpora_directory_path) if isfile(join(corpora_directory_path, x)) and corpus_file_name_pattern.match(x)]
corpus_progress_track_file_name_pattern = "progress_matrix_construction_oscarsk_{}"

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

    with open(corpus_file_path, 'r', encoding='utf-8') as corpus_file:
        for line in corpus_file:
            mycursor.close()
            mycursor = mydb.cursor()

            current_line = current_line + 1

            if current_line <= last_processed_line:
                continue
            print(f'{input_corpus_file} Processing line {str(current_line)}/{str(total_lines)} - {str(current_line/total_lines*100)}%')

            tokens = re.split('\W+', line)
            for token in tokens:
                token = token.lower()[:30]
                if token.isalpha() and token not in total_words:
                    save_word(token)
                    total_words[token] = 0

            if current_line % 100 == 0:
                print('---commiting---')
                mydb.commit()
                with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
                    progress_file.write(str(current_line))
                    progress_file.flush()
                    fsync(progress_file)

        print('---commiting---')
        mydb.commit()
        with open(progress_file_path, 'w+', encoding='utf-8') as progress_file:
            progress_file.write('-1')
            progress_file.flush()
            fsync(progress_file)

        mycursor.close()

mydb.close()
