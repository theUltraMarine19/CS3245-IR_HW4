import csv
import re
import sys
import getopt
import json
import math
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

# TODO ask if we're only allowed to submit one dictionary file => merging bigram and unigram dict together
# TODO metadata dictionary
# TODO faster computation for log frequency from Svilen
# TODO think about the benefits of stemming
# TODO check if all the memory is able to store all dictionaries before we write them out

positional_dict = {}
positional_count_dict = {}
meta_dict = {"title":{}, "date_posted":{}, "court":{}}
meta_count_dict = {"title":{}, "date_posted":{}, "court":{}}

all_doc_ids = []
ps = PorterStemmer()

doc_words1 = dict()

# the size of the training data set
collection_size = 0

csv.field_size_limit(sys.maxsize)

# params:
# -i dataset.csv -d dict.txt --dp postings.txt -p posdict.txt --pp pospostings.txt -m metadict.txt --mp metapostings.txt
# -i output/ -d dict.txt --dp postings.txt -p posdict.txt --pp pospostings.txt -m metadict.txt --mp metapostings.txt

def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file "\
                                    "-p postional-dictionary-file --pp positional-postings-file" \
                                    "-m metadata-dictionary-file --mp metadata-postings-file"


dataset_file = \
    output_pos_dict = output_pos_postings = output_meta_dict = output_meta_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:p:m:', ["pp=", "mp="])
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # dataset directory
        dataset_file = a
    elif o == '-p':  # positional dictionary file
        output_pos_dict = a
    elif o == '--pp':  # positional postings file
        output_pos_postings = a
    elif o == '-m':  # metadata dictionary file
        output_meta_dict = a
    elif o == '--mp':  # metadata postings file
        output_meta_postings = a
    else:
        assert False, "unhandled option"

if dataset_file is None \
        or output_pos_dict is None or output_pos_postings is None or output_meta_dict is None or output_meta_postings is None:
    usage()
    sys.exit(2)


def read_data_files_test(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    global collection_size
    all_docs = os.listdir(input_dir)

    for doc in all_docs:
        with open(doc, 'rb') as csv_file:
            data_reader = csv.reader(csv_file, delimiter=',', )
            for index, row in enumerate(data_reader):
                if index == 0:
                    continue
                if index >= 2:
                    break
                doc_id = row[0]
                title = row[1]
                content = row[2]
                date_posted = row[3]
                court = row[4]
                build_positional_index_dict(doc_id, content)
                build_meta_dict(doc_id, title, content, date_posted, court)
                collection_size += 1


def read_data_files(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    global collection_size
    all_docs = os.listdir(input_dir)

    os.chdir(input_dir)
    i=0
    for doc in all_docs:
        i+=1
        print i
        with open(doc, 'rb') as csv_file:
            data_reader = csv.reader(csv_file, delimiter=',', )
            for index, row in enumerate(data_reader):
                if index == 0:
                    continue
                doc_id = int(row[0])
                title = row[1]
                content = row[2]
                date_posted = row[3]
                court = row[4]
                build_positional_index_dict(doc_id, content)
                build_meta_dict(doc_id, title, content, date_posted, court)
                collection_size += 1
    os.chdir(r'..')


def build_positional_index_dict(doc_id, doc_string):
    """
    Build a positional index with a single term as key and list of dictionaries with each element having doc ID as key, and the positions in the document as values
    Positions in documents start from 1
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    count = 1
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


def build_meta_dict(doc_id, title, content, date_posted, court):
    if title not in meta_dict['title']:
        meta_dict['title'][title] = []
    meta_dict['title'][title].append(doc_id)
    if date_posted not in meta_dict['date_posted']:
        meta_dict['date_posted'][date_posted] = []
    meta_dict['date_posted'][date_posted].append(doc_id)
    if court not in meta_dict['court']:
        meta_dict['court'][court] = []
    meta_dict['court'][court].append(doc_id)


def build_positional_index_count_dict(positional_count_dict ,term='', head=0, tail=0, freq=0):
    """
    Generate the positional index with the frequency count of the terms in the right format for the dictionary file.
    :type term: the term to be inserted in the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    positional_count_dict[term] = {'H': head, 'T': tail, 'F': freq}



def build_meta_count_dict(category='', term='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param category: one of the catergories of metadata
    :param term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    meta_count_dict[category][term] = {'H': head, 'T': tail, 'F': freq}



def write_positional_output(positional_dict, positional_count_dict, output_file_dictionary, output_file_postings):
    """
    Write the positional index to output files.
    :param positional_dict:
    :param positional_count_dict:
    :param output_file_dictionary:
    :param output_file_postings:
    :return: None
    """
    with open(output_file_postings, 'w') as out_postings:
        for term, doc_id_dict in positional_dict.iteritems():
            doc_id_list = doc_id_dict.keys()
            doc_id_list.sort()

            posting = []
            for doc_id in doc_id_list:
                out_str = str(doc_id) + '-'
                pos_list = doc_id_dict[doc_id]
                pos_list.sort()
                # tf = len(pos_list)
                # out_str += str(tf) + '-'
                hold = 0
                for pos_val in pos_list:
                    if hold == 0:
                        out_str += str(pos_val)
                        hold = 1
                    else:
                        out_str += '-' + str(pos_val)
                posting.append(out_str)

            posting_str = " ".join(str(e) for e in posting) + " "

            head = out_postings.tell()
            out_postings.write(posting_str)
            freq = len(doc_id_list)
            tail = out_postings.tell()

            build_positional_index_count_dict(positional_count_dict, term, head, tail, freq)

    with open(output_file_dictionary, 'w') as out_dict:
        json.dump(positional_count_dict, out_dict)


def write_meta_output(meta_dict, meta_count_dict, output_file_dictionary, output_file_postings):
    with open(output_file_postings, 'w') as out_postings:
        for category, term_dict in meta_dict.iteritems():
            for term, posting in term_dict.iteritems():
                posting.sort()
                posting_str = " ".join(str(e) for e in posting) + " "
                head = out_postings.tell()
                out_postings.write(posting_str)
                freq = len(posting)
                tail = out_postings.tell()

                build_meta_count_dict(category, term, head, tail, freq)

    with open(output_file_dictionary, 'w') as out_dict:
        json.dump(meta_count_dict, out_dict)


if __name__ == "__main__":
    read_data_files(dataset_file)
    write_positional_output(positional_dict, positional_count_dict, output_pos_dict, output_pos_postings)
    write_meta_output(meta_dict, meta_count_dict, output_meta_dict, output_meta_postings)
