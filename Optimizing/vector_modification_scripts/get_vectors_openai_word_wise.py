import sys
import os

conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')
from corpora_modification_scripts.Util import get_unique_dataset_words

from openai import OpenAI
import json
from os import fsync

openai = OpenAI(
    # This is the default and can be omitted
    api_key="DEMO",
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
    vector_file_path = f'../resources/vector/open_ai_words_{model}.txt'

    try:
        with open(vector_file_path, 'r', encoding='utf-8') as vector_file:
            vectors = json.loads(vector_file.read())
    except FileNotFoundError:
        vectors = get_unique_dataset_words()
        for word in vectors:
            vectors[word] = []

    word_counter = 0
    word_total = len(vectors.keys())
    for word in vectors:
        word_counter = word_counter + 1

        if len(vectors[word]) > 0:
            continue

        print(f'{model} Processing line {str(word_counter)}/{str(word_total)} - {str(word_counter / word_total * 100)}%')

        vectors[word] = get_embedding(word, model)

        if word_counter % 100 == 0:
            print('---Saving---')
            with open(vector_file_path, 'w+', encoding='utf-8') as vector_file:
                vector_file.write(json.dumps(vectors))
                vector_file.flush()
                fsync(vector_file)
            print('---Saved---')

    with open(vector_file_path, 'w+', encoding='utf-8') as vector_file:
        print('---Saving---')
        vector_file.write(json.dumps(vectors))
        vector_file.flush()
        fsync(vector_file)
        print('---Saved---')



