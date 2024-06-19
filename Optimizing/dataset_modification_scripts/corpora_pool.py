# Library-like script providing pool of wrappers of available corpora

from dataset_modification_scripts.corpus_wrapper import Corpus, OscarCorpus

corpora_pool = {
    'raw': [
        OscarCorpus('oskar'),
    ],
    'lemma': [
        OscarCorpus('oskar_lemma'),
    ],
}
