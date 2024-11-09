#from googlesearch import search
import sys
sys.path.append('C:/git/STS/Optimizing/')
import json, re, wikipedia
from math import log2
from dataset_modification_scripts.lemmatize.lemmatizer_wrapper import Lemmatizer

word_pattern = re.compile('[^A-Za-z0-9áäčďéíľĺňóôŕřšśťúýźžÁÄČĎÉÍĽĹŇÓÔŔŘŠŚŤÚÝŹŽ]+')
wikipedia.set_lang("sk")

lemmatizer = Lemmatizer('../dataset_modification_scripts/')


def get_wiki_article(word):
    #search_results = list(search(word + "wikipedia sk"))
    #search_results = [x for x in search_results if not "wikipedia" in search_results]
    lemmatized_word = lemmatizer.lemmatize(word)
    search_results = wikipedia.search(lemmatized_word)
    print(word, ' ', lemmatized_word, ' ', search_results)
    content = wikipedia.page(search_results[0]).content
    content_lines = content.split('\n')
    content_lines = [line for line in content_lines if len(line) != 0 and "==" not in line]
    raw_text = word_pattern.sub(' ', ' '.join(content_lines))
    lemma_text = lemmatizer.lemmatize(raw_text)
    words = [word.lower() for word in lemma_text.split(' ') if len(word) != 0]

    return words


def get_word_occurences():
    with open('../resources/word_occurences.json', 'r', encoding='utf-8') as occ_file:
        raw_json = occ_file.read()

    return json.loads(raw_json)


def get_word_co_occurences():
    with open('../resources/word_co_occurences.json', 'r', encoding='utf-8') as occ_file:
        raw_json = occ_file.read()

    return json.loads(raw_json)


def get_word_occurences_across_paragraphs():
    with open('../resources/vector/esa_paragraphs_occured_in_counts.txt', 'r', encoding='utf-8') as occ_file:
        occurences_temp = occ_file.readlines()
    occurences = {}
    for line in occurences_temp:
        occurences[line.split(' ')[0]] = int(line.split(' ')[1])

    return occurences
word_occurences_across_paragraphs = get_word_occurences_across_paragraphs()


def get_corpora_line_count():
    with open('../resources/corpora_line_count.txt', 'r', encoding='utf-8') as corpus_line_count_file:
        line_count = int(corpus_line_count_file.read())
    return line_count
corpora_line_count = get_corpora_line_count()


def tf_idf(word, vector):
    if word not in word_occurences_across_paragraphs:
        return 0

    return tf(word, vector) * idf(word)


def tf(word, vector):
    return len([w for w in vector if w == word])


def idf(word):
    N = corpora_line_count
    Nt = word_occurences_across_paragraphs[word]
    return log2(N/Nt)
