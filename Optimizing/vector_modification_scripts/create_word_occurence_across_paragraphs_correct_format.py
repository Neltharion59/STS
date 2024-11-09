import os

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'r', encoding='utf-8') as store_file:
    file_content = store_file.read()

lines = []

current_word = ''
current_value = ''
number_chars = '0123456789'
state = 'in_word'

for character in file_content:
    if character == ' ':
        state = 'in_value'
    elif character in number_chars:
        current_value = current_value + character
    else:
        if state == 'in_value':
            state = 'in_word'
            lines.append(f'{current_word} {current_value}\n')
            current_word = ''
            current_value = ''
        elif state == 'in_word':
            current_word = current_word + character
        else:
            raise Exception

if current_word != '':
    if current_value == '':
        current_value = '0'

    lines.append(f'{current_word} {current_value}\n')

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'w', encoding='utf-8') as store_file:
    store_file.writelines(lines)
    store_file.flush()
    os.fsync(store_file)
