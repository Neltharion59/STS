# Library-like script providing wrapper class for corpus.

# Wrapper class for convenient manipulation with a single corpus
class Corpus:
    def __init__(self, name):
        self.name = name
        self.is_lemma = 'lemma' in name
        self.size = 0
        self._set_size()

    def _set_size(self):
        try:
            with open("./../resources/corpora/{}".format(self.name), 'r', encoding='utf-8') as file:
                self.size = len(file.readlines())
        except FileNotFoundError:
            pass

    def lines(self):
        with open("./../resources/corpora/{}".format(self.name), 'r', encoding='utf-8') as file:
            for line in file:
                yield line


oscar_corpus_path = "./../resources/corpora/processed/oscarsk_meta_part_{}.jsonl"
oscar_corpus_path_lemma = "./../resources/corpora/processed/oscarsk_meta_part_{}_lemma.jsonl"


class OscarCorpus(Corpus):
    def __init__(self, is_lemma):
        Corpus.__init__(self, 'oscar' if not is_lemma else 'oscar_lemma')

    def _set_size(self):
        self.size = sum(map(lambda file: len(file.readlines()), self.__files()), 0)

    def lines(self):
        for file in self.__files():
            for line in file:
                yield line

    def __files(self):
        for current_file_index in range(1, 18):
            current_oscar_corpus_path = (oscar_corpus_path if not self.is_lemma else oscar_corpus_path_lemma).format(current_file_index)
            with open(current_oscar_corpus_path, 'r', encoding='utf-8') as file:
                yield file
