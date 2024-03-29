import csv
import re
import sys
import getopt
import json
import math
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.porter import PorterStemmer

reload(sys)
sys.setdefaultencoding('ISO-8859-1')

# TODO ask if we're only allowed to submit one dictionary file => merging bigram and unigram dict together
# TODO metadata dictionary
# TODO faster computation for log frequency from Svilen
# TODO think about the benefits of stemming
# TODO check if all the memory is able to store all dictionaries before we write them out

dictionary = {}
unigram_dict = {}
unigram_count_dict = {}
bigram_dict = {}
bigram_count_dict = {}
trigram_dict = {}
trigram_count_dict = {}
positional_dict = {}
positional_count_dict = {}
meta_dict = {"title":{}, "date_posted":{}, "court":{}}
meta_count_dict = {"title":{}, "date_posted":{}, "court":{}}

all_doc_ids = []
ps = PorterStemmer()

doc_words = dict()

# the size of the training data set
collection_size = 0

csv.field_size_limit(sys.maxsize)

# params:
# -i dataset.csv -u unidict.txt --up unipostings.txt -b bidict.txt --bp bipostings.txt -t tridict.txt --tp tripostings.txt
# -p posdict.txt --pp pospostings.txt -m metadict.txt --meta-postings metapostings.txt

def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file -u unigram-dictionary-file --up unigram-postings-file "\
                                    "-b bigram-dictionary-file --bp bigram-postings-file " \
                                    "-t trigram-dictionray-file --tp trigram-postings-file" \
                                    "-p postional-dictionary-file --pp positional-postings-file" \
                                    "-m metadata-dictionary-file --mp metadata-postings-file"


dataset_file = output_uni_dict = output_uni_postings = output_bi_dict = output_bi_postings = \
    output_pos_dict = output_pos_postings = output_meta_dict = output_meta_postings = \
    output_tri_dict = output_tri_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:u:b:t:p:m:', ["up=", "bp=", "tp=", "pp=", "mp="])
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # dataset directory
        dataset_file = a
    elif o == '-u':  # unigram dictionary file
        output_uni_dict = a
    elif o == '--up':  # unigram postings file
        output_uni_postings = a
    elif o == '-b':  # bigram dictionary file
        output_bi_dict = a
    elif o == '--bp':  # bigram postings file
        output_bi_postings = a
    elif o == '-t':  # trigram dictionary file
        output_tri_dict = a
    elif o == '--tp':  # trigram postings file
        output_tri_postings = a
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

if dataset_file is None or output_uni_dict is None or output_uni_postings is None \
        or output_bi_dict is None or output_bi_postings is None \
        or output_pos_dict is None or output_pos_postings is None \
        or output_meta_dict is None or output_meta_postings is None:
    usage()
    sys.exit(2)


def read_data_files_test(input_dir):
    """
    Read from all the documents and builds the term dictionary
    :param input_dir: the path of the directory containing the training data set
    :return: None
    """
    global collection_size
    with open(input_dir, 'rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            if index == 0:
                continue
            if index >= 500:
                break
            doc_id = row[0]
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_unigram_dict(doc_id, content)
            build_bigram_dict(doc_id, content)
            build_trigram_dict(doc_id, content)
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
    with open(input_dir, 'rb') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=',', )
        for index, row in enumerate(data_reader):
            if index == 0:
                continue
            doc_id = int(row[0])
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            # content = unicode(content, errors='ignore')
            # content = content.decode(encoding='ascii', errors='ignore')
            # content.decode
            # unicode(content, errors='ignore')
            build_unigram_dict(doc_id, content)
            build_bigram_dict(doc_id, content)
            build_trigram_dict(doc_id, content)
            build_positional_index_dict(doc_id, content)
            build_meta_dict(doc_id, title, content, date_posted, court)
            collection_size += 1


def build_unigram_dict(doc_id, doc_string):
    """
    Build a unigram dictionary with a single term as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    sentences = sent_tokenize(doc_string.decode('ISO-8859-1'))
    for sent in sentences:
        words = word_tokenize(sent)
        for word in words:
            term = re.sub(r'[^a-zA-Z0-9]', '', str(word))
            term = ps.stem(term.lower())
            if len(term) != 0:
                if term in unigram_dict:
                    if doc_id in unigram_dict[term]:
                        unigram_dict[term][doc_id] += 1
                    else:
                        unigram_dict[term][doc_id] = 1
                else:
                    unigram_dict[term] = {}
                    unigram_dict[term][doc_id] = 1
                # TODO: Svilen: I assume that this code will be used for the general dictionary at the end otherwise the code underneath should be changed!
                if doc_id in doc_words:
                    if term in doc_words[doc_id]:
                        doc_words[doc_id][term] += 1
                    else:
                        doc_words[doc_id][term] = 1
                else:
                    doc_words[doc_id] = {term: 1}


def build_bigram_dict(doc_id, doc_string):
    """
    Build a bigram dictionary with a pair of terms as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    sentences = sent_tokenize(doc_string)
    for sent in sentences:
        words = word_tokenize(sent)
        for i in range(len(words) - 1):
            word1 = words[i]
            term1 = re.sub(r'[^a-zA-Z0-9]', '', str(word1))
            term1 = ps.stem(term1.lower())

            word2 = words[i+1]
            term2 = re.sub(r'[^a-zA-Z0-9]', '', str(word2))
            term2 = ps.stem(term2.lower())

            if len(term1) != 0 and len(term2) != 0:
                term = term1 + " " + term2
                if term in bigram_dict:
                    if doc_id in bigram_dict[term]:
                        bigram_dict[term][doc_id] += 1
                    else:
                        bigram_dict[term][doc_id] = 1
                else:
                    bigram_dict[term] = {}
                    bigram_dict[term][doc_id] = 1


def build_trigram_dict(doc_id, doc_string):
    """
    Build a trigram dictionary with a pair of terms as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    sentences = sent_tokenize(doc_string)
    for sent in sentences:
        words = word_tokenize(sent)
        for i in range(len(words) - 2):
            word1 = words[i]
            term1 = re.sub(r'[^a-zA-Z0-9]', '', str(word1))
            term1 = ps.stem(term1.lower())

            word2 = words[i + 1]
            term2 = re.sub(r'[^a-zA-Z0-9]', '', str(word2))
            term2 = ps.stem(term2.lower())

            word3 = words[i + 2]
            term3 = re.sub(r'[^a-zA-Z0-9]', '', str(word3))
            term3 = ps.stem(term3.lower())

            if len(term1) != 0 and len(term2) != 0 and len(term3) != 0:
                term = term1 + " " + term2 + " " + term3
                if term in trigram_dict:
                    if doc_id in trigram_dict[term]:
                        trigram_dict[term][doc_id] += 1
                    else:
                        trigram_dict[term][doc_id] = 1
                else:
                    trigram_dict[term] = {}
                    trigram_dict[term][doc_id] = 1

def build_dict(doc_id, doc_string):
    """
    Build a mixed dictionary with a pair of terms as keys and list of distinct doc IDs as values.
    :param doc_id: a document ID from the data set
    :param doc_string: the text of document corresponding to the given doc_id
    :return: None
    """
    sentences = sent_tokenize(doc_string)
    for sent in sentences:
        words = word_tokenize(sent)
        for i in range(len(words) - 2):
            word1 = words[i]
            term1 = re.sub(r'[^a-zA-Z0-9]', '', str(word1))
            term1 = ps.stem(term1.lower())

            word2 = words[i+1]
            term2 = re.sub(r'[^a-zA-Z0-9]', '', str(word2))
            term2 = ps.stem(term2.lower())

            word3 = words[i+2]
            term3 = re.sub(r'[^a-zA-Z0-9]', '', str(word3))
            term3 = ps.stem(term3.lower())

            if len(term1) != 0 and len(term2) != 0 and len(term3):
                if term1 in dictionary:
                    if doc_id in dictionary[term1]:
                        dictionary[term1][doc_id] += 1
                    else:
                        dictionary[term1][doc_id] = 1
                    if term2 in dictionary[term1]:
                        if doc_id in dictionary[term1][term2]:
                            dictionary[term1][term2][doc_id] += 1
                        else:
                            dictionary[term1][term2][doc_id] = 1
                        if term3 in dictionary[term1][term2]:
                            if doc_id in dictionary[term1][term2][term3]:
                                dictionary[term1][term2][term3][doc_id] += 1
                            else:
                                dictionary[term1][term2][term3][doc_id] = 1
                        else:
                            dictionary[term1][term2][term3] = {}
                            dictionary[term1][term2][term3][doc_id] = 1
                    else:
                        dictionary[term1][term2] = {}
                        dictionary[term1][term2][doc_id] = 1
                        dictionary[term1][term2][term3] = {}
                        dictionary[term1][term2][term3][doc_id] = 1
                else:
                    dictionary[term1] = {}
                    dictionary[term1][doc_id] = 1
                    dictionary[term1][term2] = {}
                    dictionary[term1][term2][doc_id] = 1
                    dictionary[term1][term2][term3] = {}
                    dictionary[term1][term2][term3][doc_id] = 1

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


def build_positional_index_count_dict(term='', head=0, tail=0, freq=0):
    """
    Generate the positional index with the frequency count of the terms in the right format for the dictionary file.
    :type term: the term to be inserted in the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    positional_count_dict[term] = {'H': head, 'T': tail, 'F': freq}


def build_ngram_count_dict(ngram_count_dict, term='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param ngram_count_dict:
    :type term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    ngram_count_dict[term] = {'H': head, 'T': tail, 'F': freq}


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


def write_ngram_output(ngram_dict, ngram_count_dict, output_file_dictionary, output_file_postings):
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
        doc_norm = dict()
        for term, doc_id_dict in ngram_dict.iteritems():

            doc_id_list = doc_id_dict.keys()
            doc_id_list.sort()

            posting = []
            for doc_id in doc_id_list:
                values = [1 + math.log(i, 10) for i in doc_words[doc_id].values()]
                norm_val = math.sqrt(sum(i ** 2 for i in values))
                doc_norm[doc_id] = norm_val
                posting.append(str(doc_id) + '-' + str(doc_id_dict[doc_id]))
            # add a space at the end for distinguishing the current posting string from the next posting string
            posting_str = " ".join(str(e) for e in posting) + " "

            head = out_postings.tell()
            out_postings.write(posting_str)
            freq = len(doc_id_list)
            tail = out_postings.tell()
            build_ngram_count_dict(ngram_count_dict, term, head, tail, freq)

    with open(output_file_dictionary, 'w') as out_dict:
        all_doc_ids.sort()
        ngram_count_dict['N'] = collection_size
        ngram_count_dict['DOC_NORM'] = doc_norm
        # TODO: Svilen: I don't know if we need 'ALL'. In the doc_norm, where we will store the length of a document, we will also have all docIDs
        ngram_count_dict['ALL'] = {'f': len(all_doc_ids), 'a': all_doc_ids}
        json.dump(ngram_count_dict, out_dict)


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
                tf = len(pos_list)
                out_str += str(tf) + '-'
                hold = 0
                for pos_val in pos_list:
                    if hold == 0:
                        out_str += str(pos_val)
                        hold = 1
                    else:
                        out_str += ',' + str(pos_val)
                posting.append(out_str)

            posting_str = " ".join(str(e) for e in posting) + " "

            head = out_postings.tell()
            out_postings.write(posting_str)
            freq = len(doc_id_list)
            tail = out_postings.tell()

            build_ngram_count_dict(positional_count_dict, term, head, tail, freq)

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
    read_data_files_test(dataset_file)
    write_ngram_output(unigram_dict, unigram_count_dict, output_uni_dict, output_uni_postings)
    write_ngram_output(bigram_dict, bigram_count_dict, output_bi_dict, output_bi_postings)
    write_ngram_output(trigram_dict, trigram_count_dict, output_tri_dict, output_tri_postings)
    write_positional_output(positional_dict, positional_count_dict, output_pos_dict, output_pos_postings)
    write_meta_output(meta_dict, meta_count_dict, output_meta_dict, output_meta_postings)
