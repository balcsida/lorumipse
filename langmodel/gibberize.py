#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import codecs
from basic_morphology import affix, det
from phonmodel import create_model_from_file, generate_word

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
sys.stdin = codecs.getreader('utf-8')(sys.stdin)

script_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.join(script_dir, "..", "resource")

NOUN_TRAINING = ['elekfi-nounstems-A.txt', 'elekfi-nounstems-B.txt', 'elekfi-nounstems-C.txt']
ADJ_TRAINING = ['elekfi-adjstems-A.txt', 'elekfi-adjstems-B.txt', 'elekfi-adjstems-C.txt']
VERB_TRAINING = ['elekfi-verbstems-a.txt', 'elekfi-verbstems-b.txt', 'elekfi-verbstems-c.txt']

KEPT_WORDS = [u'van', u'ez', u'az', u'kell', u'ő', u'sok', u'mi', u'amely', u'én', u'tud', u'aki', u'lehet', u'minden', u'ami',
'ki', u'olyan', u'ők', u'más', u'maga', u'mely', u'nincs', u'te', u'egyik', u'ilyen', u'való', u'fog', u'saját']

ARTICLE_SYMBOL = "#ART"

def add_resouce_dir_prefix(filenames):
    return [os.path.join(resource_dir, filename) for filename in filenames]

noun_model = create_model_from_file(add_resouce_dir_prefix(NOUN_TRAINING))
adj_model = create_model_from_file(add_resouce_dir_prefix(ADJ_TRAINING))
verb_model = create_model_from_file(add_resouce_dir_prefix(VERB_TRAINING))


sentence_delimiter_re = re.compile(r'^# \d+$')

def read_sentence(file):
    tokens = []
    for line in file:
        stripped = line.strip()
        if sentence_delimiter_re.match(stripped):
            if tokens:
                yield tokens
                tokens = []
        else:
            fields = stripped.split("\t")
            if len(fields) != 3:
                sys.stderr.write(stripped)
                raise Exception(stripped)
            tokens.append(fields)
    if tokens:
        yield tokens
    

ana_re = re.compile(r'(^|.*/)([A-Z]+)([^/]*)$')
def parse_ana(ana):
    match = ana_re.match(ana)
    if match:
        return match.group(2), match.group(3)  # pos, inflection
    else:
        sys.stderr.write(ana)
        raise Exception(ana)


def gibberize_sentence(sentence):
    generated_sentence = [generate_word_from_token(token) for token in sentence]
    generated_sentence = correct_articles(generated_sentence)
    return generated_sentence
    

def generate_word_from_token(token):
    word, lemma, ana = token
    pos, infl = parse_ana(ana)
    if pos in ["NOUN", "ADJ", "VERB"] and lemma not in KEPT_WORDS:
        gen_word = generate_word_with_ana(pos, infl)
    elif lemma == "a" and ana == "ART":
        gen_word = ARTICLE_SYMBOL
    else:
        gen_word = word
    return gen_word


def generate_word_with_ana(pos, infl):
    if pos == "NOUN":
        stem = generate_word(noun_model)
    elif pos == "ADJ":
        stem = generate_word(adj_model)
    elif pos == "VERB":
        stem = generate_word(verb_model)
    word = affix(stem, pos + infl)
    return word


def correct_articles(sentence):
    corrected_sentence = []
    for i in xrange(len(sentence)):
        word = sentence[i]
        if word == ARTICLE_SYMBOL and i + 1 < len(sentence):
            corrected_word = det(sentence[i+1])
        else:
            corrected_word = word
        corrected_sentence.append(corrected_word)
    return corrected_sentence


def print_sentence(sentence):
    print " ".join(sentence)

    
for sentence in read_sentence(sys.stdin):
    generated_sentence = gibberize_sentence(sentence)
    print_sentence([word for word, lemma, ana in sentence])
    print_sentence(generated_sentence)
    print


