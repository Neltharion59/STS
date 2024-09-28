import sys
import os

conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')
from corpora_modification_scripts.Util import get_unique_dataset_words
from dataset_modification_scripts.dataset_pool import dataset_pool
from resources.open_ai_api_key import open_ai_api_key

from openai import OpenAI
import json
from os import fsync

openai = OpenAI(
    # This is the default and can be omitted
    api_key=open_ai_api_key,
)


models = ['text-embedding-ada-002', 'text-embedding-3-small', 'text-embedding-3-large']


def get_embedding(text_to_embed, model):
    response = openai.embeddings.create(
        model=model,
        input=[text_to_embed]
    )

    data = response.data[0].embedding
    return data


for model in models:
    for dataset in dataset_pool['lemma']:
        vector_file_path = f'../resources/vector/open_ai_datasets_{model}_{dataset.name}.txt'

        already_processed_lines = 0
        try:
            with open(vector_file_path, 'r', encoding='utf-8') as vector_file:
                already_processed_lines = len(vector_file.readlines())
        except FileNotFoundError:
            pass

        lines_left, lines_right = dataset.load_dataset()

        line_counter = 0
        line_total = len(lines_left)

        if already_processed_lines >= line_total:
            continue

        buffer = []

        for line_left, line_right in zip(lines_left, lines_right):
            line_counter = line_counter + 1

            if line_counter <= already_processed_lines:
                continue

            print(f'{model} Processing line {str(line_counter)}/{str(line_total)} - {str(line_counter / line_total * 100)}%')

            left = get_embedding(line_left, model)
            right = get_embedding(line_right, model)
            new_line = '\t'.join([json.dumps(left), json.dumps(right)]) + '\n'
            buffer.append(new_line)

            if line_counter % 100 == 0:
                print('---Saving---')
                with open(vector_file_path, 'a+', encoding='utf-8') as vector_file:
                    vector_file.writelines(buffer)
                    buffer = []
                    vector_file.flush()
                    fsync(vector_file)
                print('---Saved---')

        if len(buffer) > 0:
            print('---Saving---')
            with open(vector_file_path, 'a+', encoding='utf-8') as vector_file:
                vector_file.writelines(buffer)
                buffer = []
                vector_file.flush()
                fsync(vector_file)
            print('---Saved---')



