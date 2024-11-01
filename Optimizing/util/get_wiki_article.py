#from googlesearch import search
from Optimizing.dataset_modification_scripts.lemmatize.lemmatizer_wrapper import Lemmatizer
import json, re, wikipedia

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


def get_word_occurence_across_paragraphs()