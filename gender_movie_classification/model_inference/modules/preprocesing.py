#!/usr/bin/env python3
# -*- Coding: utf-8 -*-

# https://www.nltk.org/howto/stem.html
import re
import nltk
import numpy as np
from collections import Counter
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import normalize
from sklearn.base import BaseEstimator, TransformerMixin

# Configurar el directorio de datos de nltk
nltk_data_path = '/var/task/nltk_data'
nltk.data.path.append(nltk_data_path)


class CleanText(BaseEstimator, TransformerMixin):
    def __init__(self, language_stopwords='english'):
        self.stopwords = nltk.corpus.stopwords.words(language_stopwords)

    def clean_text(self, text):
        # remove backslash-apostrophe 
        text = re.sub("\'", "", text) 
        # remove everything except alphabets 
        text = re.sub("[^a-zA-Z]"," ",text)
        # convert text to lowercase 
        return text.lower()


class TokenText(CleanText, BaseEstimator, TransformerMixin):
    def __init__(self):
        super().__init__()
        self.ps = PorterStemmer()

    def split_ps(self, text):
        text = self.clean_text(text)
        # Steming the text
        stext = [
            self.ps.stem(word)
            for word in text.split()
            if word not in self.stopwords
        ]
        return ' '.join(stext)

    def clean_texts(self, texts):
        return texts.apply(self.clean_text)

    def transform(self, texts):
        return texts.apply(self.split_ps)

    def fit(self, X, y=None):
        return self


class ToDense(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def vstack(self, vect):
        return np.vstack(vect)

    def transform(self, vect):
        return np.asarray(vect.todense())

    def fit(self, X, y=None):
        return self


class Normalize(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, vect):
        return normalize(X=vect)

    def fit(self, X, y=None):
        return self


class TextToDictTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return [Counter(re.findall(r'\b\w+\b', text)) for text in X]
