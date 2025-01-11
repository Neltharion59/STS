# Runnable script lematizing corpora, creating new versions of corpora (does not overwrite original corpuss)

import sys
import os

conf_path = os.getcwd()
sys.path.append('D:/git/STS/Optimizing/')

import concurrent
import os
from os import listdir
from os.path import isfile, join
import re
import sys
from dataset_modification_scripts.lemmatize.lemmatizer_wrapper import Lemmatizer
from concurrent.futures import ThreadPoolExecutor, as_completed

lemmatizer = Lemmatizer()


# Lemmatize given text using lemmatizer API
# Params: str
# Return: str
def lemmatize(text):
    return lemmatizer.lemmatize(text)


# Let's prepare the paths to read from and write to.
input_path = "./../resources/corpora/processed/"
output_path = "./../resources/corpora/processed/"

# Let's prepare regexes to be used throughout this script.
corpus_input_file_name_pattern = re.compile("oscarsk_meta_part_[0-9]+.jsonl")

# Let's prepare list of corpus files to be lemmatized.
input_corpus_files = [x for x in listdir(input_path) if isfile(join(input_path, x)) and corpus_input_file_name_pattern.match(x)]

def process_single_file(input_corpus_file):
    try:
        # Prepare full path to both input and output file
        output_corpus_file = output_path + input_corpus_file.replace(".jsonl", "_sk_lemma.jsonl")
        counter_file_path = output_path + input_corpus_file.replace(".jsonl", "_sk_lemma_counter.txt")
        input_corpus_file = input_path + input_corpus_file

        print(input_corpus_file)

        # Let's see how many lines of the corpus are already lemmatized
        try:
            with open(counter_file_path, "r", encoding='utf-8') as counter_file:
                processed_line_count = int(counter_file.read())
        except FileNotFoundError:
            processed_line_count = 0

        print('Lines processed beforehand: ' + str(processed_line_count))
        current_line_counter = 0
        batch = ""
        # Let's loop over all lines of the corpus
        with open(input_corpus_file, 'r', encoding='utf-8') as input_file:
            buffer = []

            for line in input_file:
                current_line_counter = current_line_counter + 1
                # If this line is already processed, let's not process it again
                if current_line_counter <= processed_line_count:
                    continue

                print("{}: Processing line {}".format(input_corpus_file, current_line_counter))

                # Let's split the line to tokens (similarity score, text1, text2)
                lemmatized_text = lemmatize(line) + '\n'

                buffer.append(lemmatized_text)

                if current_line_counter % 100 == 0:

                    with open(output_corpus_file, "a+", encoding='utf-8') as output_file:
                        output_file.writelines(buffer)
                        buffer = []
                        output_file.flush()
                        os.fsync(output_file)

                    with open(counter_file_path, "w+", encoding='utf-8') as counter_file:
                        counter_file.write(str(current_line_counter))
                        counter_file.flush()
                        os.fsync(counter_file)

            with open(output_corpus_file, "a+", encoding='utf-8') as output_file:
                output_file.writelines(buffer)
                buffer = []
                output_file.flush()
                os.fsync(output_file)

            with open(counter_file_path, "w+", encoding='utf-8') as counter_file:
                counter_file.write(str(current_line_counter))
                counter_file.flush()
                os.fsync(counter_file)
    except:
        playsound('./../sounds/wrong.mp3')
        raise sys.exc_info()[0]


if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(process_single_file, data): data for data in input_corpus_files}

        for future in as_completed(futures):
            data = futures[future]
            try:
                print(f"Completed {data}")
            except Exception as exc:
                print(f"Data {data} generated an exception: {exc}")
