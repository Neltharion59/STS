import sys
import os
import mysql.connector

conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

feature_word_file = './../resources/feature_words.txt'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="sts_data",
  charset='utf8',
  use_unicode=True
)

mycursor = mydb.cursor()


def get_word_text(word_id):
    sql_get = f"SELECT word.text FROM word WHERE word.id = {word_id};"
    mycursor.execute(sql_get)
    myresult = mycursor.fetchall()
    return myresult[0][0]


with open(feature_word_file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

line_counter = 0
new_lines = []
for line in lines:
    line_counter = line_counter + 1
    tokens = line.split()
    print(line_counter)
    word_id = tokens[0]
    freq = tokens[1]
    word_text = get_word_text(word_id)
    new_line = ' '.join([word_text, word_id, freq]) + '\n'
    new_lines.append(new_line)

with open(feature_word_file, 'w', encoding='utf-8') as file:
    lines = file.writelines(new_lines)
