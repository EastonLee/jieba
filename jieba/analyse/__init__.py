from __future__ import absolute_import
from .tfidf import TFIDF
from .textrank import TextRank
import jieba
#easton: cost a lot of time
import jieba.posseg
import os
from operator import itemgetter
from .textrank import textrank
try:
    from .analyzer import ChineseAnalyzer
except ImportError:
    pass

default_tfidf = TFIDF()
default_textrank = TextRank()

extract_tags = tfidf = default_tfidf.extract_tags
set_idf_path = default_tfidf.set_idf_path
textrank = default_textrank.extract_tags
STOP_WORDS = set((
    "the","of","is","and","to","in","that","we","for","an","are",
    "by","be","as","on","with","can","if","from","which","you","it",
    "this","then","at","have","all","not","one","has","or","that"
))

class IDFLoader:
    def __init__(self):
        self.path = ""
        self.idf_freq = {}
        self.median_idf = 0.0

    def set_new_path(self, new_idf_path):
        if self.path != new_idf_path:
            content = open(new_idf_path, 'rb').read().decode('utf-8')
            idf_freq = {}
            lines = content.rstrip('\n').split('\n')
            #easton: cost time
            for line in lines:
                word, freq = line.split(' ')
                idf_freq[word] = float(freq)
            median_idf = sorted(idf_freq.values())[len(idf_freq)//2]
            self.idf_freq = idf_freq
            self.median_idf = median_idf
            self.path = new_idf_path

    def get_idf(self):
        return self.idf_freq, self.median_idf

idf_loader = IDFLoader()
#easton: cost time
idf_loader.set_new_path(abs_path)

def set_idf_path(idf_path):
    new_abs_path = os.path.normpath(os.path.join(os.getcwd(), idf_path))
    if not os.path.exists(new_abs_path):
        raise Exception("jieba: path does not exist: " + new_abs_path)
    idf_loader.set_new_path(new_abs_path)

def set_stop_words(stop_words_path):
    default_tfidf.set_stop_words(stop_words_path)
    default_textrank.set_stop_words(stop_words_path)
