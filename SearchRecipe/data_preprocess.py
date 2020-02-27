# -*- coding: utf-8 -*-
# @Time    : 2019-10-11 00:06
# @Author  : jinhang
# @File    : data_preprocess.py

from nltk.stem.porter import *
import re
import os
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cw3site.settings')
stop_path = os.path.join(settings.STATICFILES_DIRS[0], "englishST.txt")


def case_folding(text):
    """
    make the characters in document and queries be lower case

    :param text: input characters
    :return: lower case characters
    """
    text = text.lower()
    return text


def tokenisation(text):
    """
    get tokens from text, just split on every non-letter character

    :param text: can be document or queries in ranked query
    :return: get tokens
    """
    # text = re.sub('[^\w\d]', ' ', text)
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.split()
    return text


def stopping(tokens):
    """
    remove the stop words in tokens

    :param tokens: the tokens got from tokenisation function
    :return: tokens without stop words
    """
    stopwords = set()
    with open(stop_path) as f:
        for line in f:
            stopwords.add(line.strip('\n'))
    tokens = [x for x in tokens if x not in stopwords]
    return tokens


def stemming(token_list):
    """
    change the tokens into stem form

    :param token_list: the tokens got from stopping
    :return: tokens with stem form
    """
    stemmer = PorterStemmer()
    norm_tokens = [stemmer.stem(token) for token in token_list]
    return norm_tokens



