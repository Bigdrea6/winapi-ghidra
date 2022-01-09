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
algo = "sum"

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


if __name__ == "__main__":
    en_text = """Yuriko Koike cruised to a resounding victory in the gubernatorial election July 5,securing a second term and marking the end of a predictable campaign held during unpredictable times.
The incumbent, who turns 68 on July 15,
was pitted against a slew of lesser-known candidates in a campaign overshadowed by the unnerving presence of a pandemic.
Koike’s vote total of 3,661,371 was more than four times higher than that of her closest challenger,
a sign that a majority of voters in Tokyo trust her to continue the battle against the novel coronavirus.
Kenji Utsunomiya, a 73-year-old lawyer and former head of the Japan Federation of Bar Associations,
won only 844,151 votes. Taro Yamamoto, 45, an actor-turned-leader of anti-establishment party Reiwa Shinsengumi,
finished third with 657,277 votes. Election turnout was 55%, down from 59% in the 2016 poll.
Koike said she aims to focus her efforts on preventing and preparing for a possible second wave of the novel coronavirus by enhancing testing capacity,
increasing the number of hospital beds and bolstering the city’s health care system. She also said she aims to establish Tokyo’s own center for disease control,
akin to the Centers for Disease Control and Prevention (CDC) in the U.S.,
to consolidate the city’s response to the virus and stage a “simplified” Olympics next year."""
    
    sum_sentences = summarize_sentences(en_text)
    print(sum_sentences)