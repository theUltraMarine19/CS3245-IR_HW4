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

unigram_dict = {}
unigram_count_dict = {}
meta_dict = {"title":{}, "date_posted":{}, "court":{}}
meta_count_dict = {"title":{}, "date_posted":{}, "court":{}}
stemmer_dict = {}

all_doc_ids = []
ps = PorterStemmer()

doc_words = {}

# the size of the training data set
collection_size = 0

csv.field_size_limit(sys.maxsize)

output_meta_dict = "metadict.txt"
output_meta_postings = "metapostings.txt"

# params:
# -i dataset.csv -d dict.txt -p postings.txt

def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file -d unigram-dictionary-file -p unigram-postings-file "


dataset_file = output_unigram_dict = output_unigram_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # dataset directory
        dataset_file = a
    elif o == '-d':  # unigram dictionary file
        output_unigram_dict = a
    elif o == '-p':  # unigram postings file
        output_unigram_postings = a
    else:
        assert False, "unhandled option"

if dataset_file is None or output_unigram_dict is None or output_unigram_postings is None:
    usage()
    sys.exit(2)


def read_data_files_test(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    global collection_size
    count = 0

    with open(input_dir, 'rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            if index == 0:
                continue
            if index >= 10:
                break
            doc_id = row[0]
            print count
            count = count + 1
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_unigram_dict(doc_id, content)
            build_meta_dict(doc_id, title, content, date_posted, court)
            collection_size += 1


def read_data_files(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    global collection_size
    count = 0

    with open(input_dir, 'rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            if index == 0:
                continue
            doc_id = row[0]
            print count
            count = count + 1
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_unigram_dict(doc_id, content)
            build_meta_dict(doc_id, title, content, date_posted, court)
            collection_size += 1

def build_unigram_dict(doc_id, doc_string):
    """
    Build a mixed dictionary with a pair of terms as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    sentences = sent_tokenize(doc_string)
    for sent in sentences:
        words = word_tokenize(sent)
        for i in range(len(words)):
            word1 = words[i]
            term = re.sub(r'[^a-zA-Z0-9]', '', str(word1))
            term = term.lower()

            cache = stemmer_dict.get(term, None)
            if cache is not None:
                term = cache
            else:
                stem_res = ps.stem(term)
                stemmer_dict[term] = stem_res
                term = stem_res

            if len(term) != 0:
                if term in unigram_dict:
                    if doc_id in unigram_dict[term]:
                        unigram_dict[term][doc_id] += 1
                    else:
                        unigram_dict[term][doc_id] = 1
                else:
                    unigram_dict[term] = {}
                    unigram_dict[term][doc_id] = 1

                # build the length add-on to the free text retrieval
                if doc_id in doc_words:
                    if term in doc_words[doc_id]:
                        doc_words[doc_id][term] += 1
                    else:
                        doc_words[doc_id][term] = 1
                else:
                    doc_words[doc_id] = {term: 1}


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



def build_unigram_dictionary_count_dict(ngram_dictionary_count_dict, term='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param ngram_count_dict:
    :type term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    ngram_dictionary_count_dict[term] = {'H': head, 'T': tail, 'F': freq}


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


def write_unigram_dict_output(ngram_dict, ngram_count_dict, output_file_dictionary, output_file_postings):
    """
    Write the term count dictionary and the postings file to 2 distinct txt files.
    :param ngram_dict:
    :param ngram_count_dict:
    :param output_file_dictionary:
    :param output_file_postings:
    :return: None
    """
    with open(output_file_postings, 'w') as out_postings:
        # term_dict has term as key, doc_id_dict as value
        # doc_id_dict has doc id as key, term frequency corresponding to the doc id as value
        doc_norm = {}

        for term, doc_id_dict in ngram_dict.iteritems():
            unigram_posting = []

            for term_or_doc_id, dict_or_tf in doc_id_dict.iteritems():
                    # handle unigram
                    if term_or_doc_id not in doc_norm:
                        values = [1 + math.log(i, 10) for i in doc_words[term_or_doc_id].values()]
                        norm_val = math.sqrt(sum(i ** 2 for i in values))
                        doc_norm[term_or_doc_id] = norm_val
                    unigram_posting.append(str(term_or_doc_id) + '-' + str(dict_or_tf))
            
            posting_str = " ".join(str(e) for e in unigram_posting) + " "

            head = out_postings.tell()
            out_postings.write(posting_str)
            freq = len(unigram_posting)
            tail = out_postings.tell()
            build_unigram_dictionary_count_dict(unigram_count_dict, term, head, tail, freq)

    with open(output_file_dictionary, 'w') as out_dict:
        ngram_count_dict['N'] = collection_size
        ngram_count_dict['DOC_NORM'] = doc_norm
        json.dump(unigram_count_dict, out_dict)


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
    write_unigram_dict_output(unigram_dict, unigram_count_dict, output_unigram_dict, output_unigram_postings)
    write_meta_output(meta_dict, meta_count_dict, output_meta_dict, output_meta_postings)