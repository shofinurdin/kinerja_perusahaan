
from PyPDF2 import PdfReader
from nltk.tokenize import word_tokenize
import nltk
import string
import csv
import re
import os
import pandas as pd



# preprocessing
def text_prepros(text):

    # converting to lowercase
    text = text.lower()

    # remove tab, new line, dan backslash
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\'," ")

    # remove non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii') #encode get original character, ex: poke'mon

    # remove link hastag
    text = ' '.join(re.sub('([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)', ' ', text).split())

    # remove incomplete url
    text = text.replace('http://', ' ').replace('https://', ' ')

    # remove puctuation
    text = text.translate(str.maketrans(' ',' ',string.punctuation))

    # remove whitespace leading & trailing
    text = text.strip()

    # substituting multiple spaces with single space
    text = re.sub(r'\s+', ' ', text, flags=re.I)

    # remove number
    text = re.sub(r'\d+', ' ', text)

    # remove all the special characters
    text = re.sub(r'\W', ' ', text)

    # remove single char
    text = re.sub(r"\b[a-zA-Z]\b", "", text)

    # remove all single characters
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)

    # remove single characters from the start
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)

    return text

# tokenize
def word_tokenize_wrapper(text):
    return word_tokenize(text)

# read csv to dict
def lexicon_to_dict(path, delimiter="\s", has_header=False):
    item = {}
    with open(path, "r") as n:
        # read csv row
        reader_format = csv.reader(n, delimiter=delimiter)

        # skip header
        if has_header:
            next(reader_format)

        # add dictio item
        for row in reader_format:
            item[row[0]] = row[1]

    return item

# determine non financial variable
def non_financial(FILENAME, TAHUN, text, lexicon):

    result = {'file_name': FILENAME, 'tahun': TAHUN}
    score_positive, score_negative, score_uncertainty, score_litigious, score_strongModal, score_weakModal, score_constraining = 0, 0, 0, 0, 0, 0, 0
    hit_positive, hit_negative, hit_uncertainty, hit_litigious, hit_strongModal, hit_weakModal, hit_constraining = [], [], [], [], [], [], []

    for word in text:
        for term in lexicon:
            if word == term:
#                 print(term, lexicon[term])
                if lexicon[term] == "Positive":
                    score_positive += 1
                    result["score_positive"] = score_positive
                    hit_positive.append(term)
                    hit_positive.sort()
#                     result["hit_positive"] = hit_positive
                elif lexicon[term] == "Negative":
                    score_negative += 1
                    result["score_negative"] = score_negative
                    hit_negative.append(term)
                    hit_negative.sort()
#                     result["hit_negative"] = hit_negative
                elif lexicon[term] == "Uncertainty":
                    score_uncertainty += 1
                    result["score_uncertainty"] = score_uncertainty
                    hit_uncertainty.append(term)
                    hit_uncertainty.sort()
#                     result["hit_uncertainty"] = hit_uncertainty
                elif lexicon[term] == "Litigious":
                    score_litigious += 1
                    result["score_litigious"] = score_litigious
                    hit_litigious.append(term)
                    hit_litigious.sort()
#                     result["hit_litigious"] = hit_litigious
                elif lexicon[term] == "StrongModal":
                    score_strongModal += 1
                    result["score_strongModal"] = score_strongModal
                    hit_strongModal.append(term)
                    hit_strongModal.sort()
#                     result["hit_strongModal"] = hit_strongModal
                elif lexicon[term] == "WeakModal":
                    score_weakModal += 1
                    result["score_weakModal"] = score_weakModal
                    hit_weakModal.append(term)
                    hit_weakModal.sort()
#                     result["hit_weakModal"] = hit_weakModal
                elif lexicon[term] == "Constraining":
                    score_constraining += 1
                    result["score_constraining"] = score_constraining
                    hit_constraining.append(term)
                    hit_constraining.sort()
#                     result["hit_constraining"] = hit_constraining

    return result