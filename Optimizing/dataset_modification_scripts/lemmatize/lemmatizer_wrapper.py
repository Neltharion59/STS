import ufal.udpipe
from functools import reduce
model_path = './lemmatize/slovak-snk-ud-2.5-191206.udpipe'

class Lemmatizer:
    def __init__(self):
        self.lemmatization_model = self.__load_model(model_path)

    def lemmatize(self, text):
        sentences = self.__process(self.lemmatization_model, text)
        self.__lemmatize(self.lemmatization_model, sentences)
        merged = ' '.join(list(self.__extract_lemmas(sentences)))
        return merged

    def __load_model(self, model_path):
        model = ufal.udpipe.Model.load(model_path)
        if not model:
            raise Exception("Cannot load UDPipe model from file '%s'" % model_path)
        return model

    def __process(self, model, text):
        tokenizer = model.newTokenizer(ufal.udpipe.Model.DEFAULT)
        if not tokenizer:
            raise Exception("Cannot create tokenizer")

        tokenizer.setText(text)
        sentences = []
        sentence = ufal.udpipe.Sentence()
        while tokenizer.nextSentence(sentence):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()

        return sentences

    def __process(self, model, text):
        tokenizer = model.newTokenizer(ufal.udpipe.Model.DEFAULT)
        if not tokenizer:
            raise Exception("Cannot create tokenizer")

        tokenizer.setText(text)
        sentences = []
        sentence = ufal.udpipe.Sentence()
        while tokenizer.nextSentence(sentence):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()

        return sentences

    def __lemmatize(self, model, sentences):
        for sentence in sentences:
            model.tag(sentence, model.DEFAULT)
            model.parse(sentence, model.DEFAULT)

    def __extract_lemmas(self, sentences):
        for sentence in sentences:
            for word in sentence.words[1:]:  # Skipping the root element
                yield word.lemma
