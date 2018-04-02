# -*- coding: utf-8 -*-
import csv
import re
import sys
import getopt
import json
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

unigram_dict = {}
unigram_count_dict = {}
bigram_dict = {}
bigram_count_dict = {}
positional_dict = {}
positional_count_dict = {}

all_doc_ids = []
ps = PorterStemmer()


# -i dataset.csv -u unidict.txt --uni-postings unipostings.txt -b bidict.txt --bi-postings bipostings.txt
def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file -u unigram-dictionary-file --uni-postings unigram-postings-file "\
                                    "-b bigram-dictionary-file --bi-postings bigram-postings-file"


dataset_file = output_uni_dict = output_uni_postings = output_bi_dict = output_bi_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:u:b:', ["uni-postings", "bi-postings"])
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # dataset directory
        dataset_file = a
    elif o == '-u':  # unigram dictionary file
        output_uni_dict = a
    elif o == '--uni-postings':  # unigram postings file
        output_uni_postings = a
    elif o == '-b':  # bigram dictionary file
        output_bi_dict = a
    elif o == '--bi-postings':  # bigram postings file
        output_bi_postings = a
    else:
        assert False, "unhandled option"


print dataset_file, output_uni_dict, output_uni_postings, output_bi_dict, output_bi_postings

# TODO Need to parse --flags properly
# if dataset_file is None or output_uni_dict is None or output_uni_postings is None \
#         or output_bi_dict is None or output_bi_postings is None:
#     usage()
#     sys.exit(2)


def read_data_files_test(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    with open('dataset.csv','rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            if index == 1:
                continue
            if index >= 50:
                break
            doc_id = row[0]
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_unigram_dict()
            build_bigram_dict()




def read_data_files(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    with open('dataset.csv','rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            doc_id = row[0]
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_unigram_dict()
            build_bigram_dict()


def build_unigram_dict(doc_id, doc_string):
    """
    Build a unigram dictionary with a single term as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """

def build_unigram_count_dict(term='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :type term: the term to be added to the dictionary
    :return: None
    """

def build_bigram_dict(doc_id, doc_string):
    """
    Build a bigram dictionary with a pair of terms as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """

def build_bigram_count_dict(term='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :type term: the term to be added to the dictionary
    :return: None
    """

def build_positional_index_dict(doc_id, doc_string):
    """
    Build a positional index with a single term as key and list of dictionaries with each element having doc ID as key, and the positions in the document as values
    Positions in documents start from 1
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    count = 0
    sentences = sent_tokenize(doc_string)
    for sent in sentences:
        words = word_tokenize(sent)
        for word in words:
            term = re.sub(r'[^a-zA-Z0-9]', '', str(word))
            term = ps.stem(term.lower())
            if len(term) != 0:
                if term in positional_dict:
                    if doc_id not in positional_dict[term]:
                        positional_dict[term][doc_id] = [count]
                    else:
                         positional_dict[term][doc_id].append(count)
                else:
                    positional_dict[term] = {}
                    positional_dict[term][doc_id] = [count]
            count += 1

def write_output():
    """
    Write the term count dictionary, doc length dictionary, and the postings file to 3 distinct txt files.
    :return: None
    """


if __name__ == "__main__":
    read_data_files_test(dataset_file)
