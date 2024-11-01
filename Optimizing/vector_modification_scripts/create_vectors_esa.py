import sys
sys.path.append('D:/git/STS/Optimizing/')
from corpora_modification_scripts.Util import split_to_words, get_unique_dataset_words
from util.get_wiki_article import get_wiki_article, get_word_occurences, get_word_co_occurences

vector_words = [word for word in get_unique_dataset_words()]

for word in vector_words:
    wiki_words = get_wiki_article(word)
    print(wiki_words)
    print(len(wiki_words))
    exit(0)