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


# -i dataset.csv -u unidict.txt -b bidict.txt --uni-postings unipostings.txt --bi-postings bipostings.txt
def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file -u unigram-dictionary-file --uni-postings unigram-postings-file "\
                                    "-b bigram-dictionary-file --bi-postings bigram-postings-file"

dataset_file = output_uni_dict = output_uni_postings = output_bi_dict = output_bi_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:l:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # input directory
        dataset_file = a
    elif o == '-u':  # dictionary file
        output_uni_dict = a
    elif o == '--uni-postings':  # postings file
        output_file_postings = a
    elif o == '-b':  # document length file
        output_file_doc_length = a
    else:
        assert False, "unhandled option"

if dataset_file is None or output_file_postings is None or output_uni_dict is None or output_file_doc_length is None:
    usage()
    sys.exit(2)


def read_data_files_test(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    i = 0
    with open('dataset.csv','rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for row in data_reader:
            if i > 50:
                break
            print row
            i += 1


def read_data_files(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    with open('dataset.csv','rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for row in data_reader:
            print row


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

def write_output():
    """
    Write the term count dictionary, doc length dictionary, and the postings file to 3 distinct txt files.
    :return: None
    """


if __name__ == "__main__":
    read_data_files_test(dataset_file)
