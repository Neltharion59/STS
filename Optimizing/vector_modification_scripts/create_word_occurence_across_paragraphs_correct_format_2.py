import os

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'r', encoding='utf-8') as store_file:
    lines = store_file.readlines()

for line in lines:
    print(line)
exit(0)

with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'w', encoding='utf-8') as store_file:
    store_file.writelines(lines)
    store_file.flush()
    os.fsync(store_file)
