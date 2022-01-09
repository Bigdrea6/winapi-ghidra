import spacy
import neologdn
import re
import emoji
import mojimoji

class EnglishCorpus:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def preprocessing(self, text):
        text = re.sub(r'\n', '', text)
        text = re.sub(r'\r', '', text)
        text = mojimoji.han_to_zen(text, digit=False, ascii=False)
        text = mojimoji.zen_to_han(text, kana=True)
        text = ''.join(c for c in text if c not in emoji.UNICODE_EMOJI)
        text = neologdn.normalize(text)
        return text
    
    def make_sentence_list(self, sentences):
        doc = self.nlp(sentences)
        self.ginza_sents_object = doc.sents
        sentence_list = [s for s in doc.sents]
        return sentence_list

    def make_corpus(self):
        corpus = []
        for s in self.ginza_sents_object:
            tokens = [str(t) for t in s]
            corpus.append(' '.join(tokens))
        return corpus

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words

from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer

algorithm_dic = {
    "lex": LexRankSummarizer(), "tex": TextRankSummarizer(),
    "lsa": LsaSummarizer(), "kl": KLSummarizer(), "luhn": LuhnSummarizer(),
    "redu": ReductionSummarizer(), "sum": SumBasicSummarizer()
}

language = "english"
sentences_count = 1
algo = "lex"

def summarize_sentences(sentences):
    corpus_maker = EnglishCorpus()
    preprocessed_sentences = corpus_maker.preprocessing(sentences)
    preprocessed_sentence_list = corpus_maker.make_sentence_list(preprocessed_sentences)
    corpus = corpus_maker.make_corpus()
    parser = PlaintextParser.from_string(" ".join(corpus), Tokenizer(language))

    summarizer = algorithm_dic[algo]
    summarizer.stop_words = get_stop_words(language)
    summary = summarizer(document=parser.document, sentences_count=sentences_count)
    return " ".join([sentence.__str__() for sentence in summary])