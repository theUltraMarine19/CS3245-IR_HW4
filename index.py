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

ngram_dictionary = {}
ngram_dictionary_count_dict = {}
positional_dict = {}
positional_count_dict = {}
meta_dict = {"title":{}, "date_posted":{}, "court":{}}
meta_count_dict = {"title":{}, "date_posted":{}, "court":{}}

all_doc_ids = []
ps = PorterStemmer()

doc_words1 = dict()
doc_words2 = dict()
doc_words3 = dict()

# the size of the training data set
collection_size = 0

csv.field_size_limit(sys.maxsize)

# params:
# -i dataset.csv -d dict.txt --dp postings.txt -p posdict.txt --pp pospostings.txt -m metadict.txt --mp metapostings.txt

def usage():
    print "usage: " + sys.argv[0] + " -i dataset_file -d ngram-dictionary-file --dp ngram-postings-file "\
                                    "-m metadata-dictionary-file --mp metadata-postings-file"


dataset_file = output_ngram_dict = output_ngram_postings = \
    output_meta_dict = output_meta_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:m:', ["dp=", "mp="])
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i':  # dataset directory
        dataset_file = a
    elif o == '-d':  # unigram dictionary file
        output_ngram_dict = a
    elif o == '--dp':  # unigram postings file
        output_ngram_postings = a
    # elif o == '-p':  # positional dictionary file
    #     output_pos_dict = a
    # elif o == '--pp':  # positional postings file
    #     output_pos_postings = a
    elif o == '-m':  # metadata dictionary file
        output_meta_dict = a
    elif o == '--mp':  # metadata postings file
        output_meta_postings = a
    else:
        assert False, "unhandled option"

if dataset_file is None or output_ngram_dict is None or output_ngram_postings is None \
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
            if index >= 2:
                break
            doc_id = row[0]
            title = row[1]
            content = row[2]
            date_posted = row[3]
            court = row[4]
            build_ngram_dict(doc_id, content)
            # build_positional_index_dict(doc_id, content)
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
            build_ngram_dict(doc_id, content)
            build_positional_index_dict(doc_id, content)
            build_meta_dict(doc_id, title, content, date_posted, court)
            collection_size += 1

def build_ngram_dict(doc_id, doc_string):
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
            term1 = re.sub(r'[^a-zA-Z0-9]', '', str(word1))
            term1 = ps.stem(term1.lower())

            if len(term1) != 0:
                if term1 in ngram_dictionary:
                    if doc_id in ngram_dictionary[term1]:
                        ngram_dictionary[term1][doc_id] += 1
                    else:
                        ngram_dictionary[term1][doc_id] = 1
                else:
                    ngram_dictionary[term1] = {}
                    ngram_dictionary[term1][doc_id] = 1

                if i <= (len(words) - 2):
                    word2 = words[i+1]
                    term2 = re.sub(r'[^a-zA-Z0-9]', '', str(word2))
                    term2 = ps.stem(term2.lower())

                    if len(term2) != 0:
                        if term2 in ngram_dictionary[term1]:
                            if doc_id in ngram_dictionary[term1][term2]:
                                ngram_dictionary[term1][term2][doc_id] += 1
                            else:
                                ngram_dictionary[term1][term2][doc_id] = 1
                        else:
                            ngram_dictionary[term1][term2] = {}
                            ngram_dictionary[term1][term2][doc_id] = 1

                        if i <= (len(words) - 3):
                            word3 = words[i+2]
                            term3 = re.sub(r'[^a-zA-Z0-9]', '', str(word3))
                            term3 = ps.stem(term3.lower())

                            if len(term3) != 0:
                                if term3 in ngram_dictionary[term1][term2]:
                                    if doc_id in ngram_dictionary[term1][term2][term3]:
                                        ngram_dictionary[term1][term2][term3][doc_id] += 1
                                    else:
                                        ngram_dictionary[term1][term2][term3][doc_id] = 1
                                else:
                                    ngram_dictionary[term1][term2][term3] = {}
                                    ngram_dictionary[term1][term2][term3][doc_id] = 1

                                if doc_id in doc_words3:
                                    if term1 + " " + term2 + " " + term3 in doc_words3[doc_id]:
                                        doc_words3[doc_id][term1 + " " + term2 + " " + term3] += 1
                                    else:
                                        doc_words3[doc_id][term1 + " " + term2 + " " + term3] = 1
                                else:
                                    doc_words3[doc_id] = {term1 + " " + term2 + " " + term3: 1}

                        if doc_id in doc_words2:
                            if term1 + " " + term2 in doc_words2[doc_id]:
                                doc_words2[doc_id][term1 + " " + term2] += 1
                            else:
                                doc_words2[doc_id][term1 + " " + term2] = 1
                        else:
                            doc_words2[doc_id] = {term1 + " " + term2: 1}

                # build the length add-on to the free text retrieval
                if doc_id in doc_words1:
                    if term1 in doc_words1[doc_id]:
                        doc_words1[doc_id][term1] += 1
                    else:
                        doc_words1[doc_id][term1] = 1
                else:
                    doc_words1[doc_id] = {term1: 1}


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


def build_unigram_dictionary_count_dict(ngram_dictionary_count_dict, term1='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param ngram_count_dict:
    :type term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    if term1 in ngram_dictionary_count_dict:
        ngram_dictionary_count_dict[term1]['H'] = head
        ngram_dictionary_count_dict[term1]['T'] = tail
        ngram_dictionary_count_dict[term1]['F'] = freq
    else:
        ngram_dictionary_count_dict[term1] = {'H': head, 'T': tail, 'F': freq}

def build_bigram_dictionary_count_dict(ngram_dictionary_count_dict, term1='', term2 ='', head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param ngram_count_dict:
    :type term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    if term1 not in ngram_dictionary_count_dict:
        ngram_dictionary_count_dict[term1] = {}

    if term2 in ngram_dictionary_count_dict[term1]:
        ngram_dictionary_count_dict[term1][term2]['H'] = head
        ngram_dictionary_count_dict[term1][term2]['T'] = tail
        ngram_dictionary_count_dict[term1][term2]['F'] = freq
    else:
        ngram_dictionary_count_dict[term1][term2] = {'H': head, 'T': tail, 'F': freq}

def build_trigram_dictionary_count_dict(ngram_dictionary_count_dict, term1='', term2 ='', term3 = '',head=0, tail=0, freq=0):
    """
    Build the dictionary with term as keys and the frequency count, head and tail byte location as values.
    :param ngram_count_dict:
    :type term: the term to be added to the dictionary
    :param head:
    :param tail:
    :param freq:
    :return: None
    """
    if term1 not in ngram_dictionary_count_dict:
        ngram_dictionary_count_dict[term1] = {}
    if term2 not in ngram_dictionary_count_dict[term1]:
        ngram_dictionary_count_dict[term1][term2] = {}
    ngram_dictionary_count_dict[term1][term2][term3] = {'H': head, 'T': tail, 'F': freq}



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



def write_ngram_dict_output(ngram_dict, ngram_count_dict, output_file_dictionary, output_file_postings):
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
        doc_norm1 = {}
        doc_norm2 = {}
        doc_norm3 = {}

        for term1, doc_id_dict1 in ngram_dict.iteritems():
            unigram_posting = []

            for term_or_doc_id1, dict_or_tf1 in doc_id_dict1.iteritems():
                if type(dict_or_tf1) is dict:
                    term2 = term_or_doc_id1
                    bigram_posting = []

                    for term_or_doc_id2, dict_or_tf2 in dict_or_tf1.iteritems():
                        if type(dict_or_tf2) is dict:
                            # handle trigram
                            term3 = term_or_doc_id2
                            trigram_posting = []

                            for term_or_doc_id3, dict_or_tf3 in dict_or_tf2.iteritems():
                                if term_or_doc_id3 not in doc_norm3:
                                    values3 = [1 + math.log(i, 10) for i in doc_words3[term_or_doc_id3].values()]
                                    norm_val3 = math.sqrt(sum(i ** 2 for i in values3))
                                    doc_norm3[term_or_doc_id3] = norm_val3
                                trigram_posting.append(str(term_or_doc_id3) + '-' + str(dict_or_tf3))

                            posting_str3 = " ".join(str(e) for e in trigram_posting) + " "

                            head3 = out_postings.tell()
                            out_postings.write(posting_str3)
                            freq3 = len(trigram_posting)
                            tail3 = out_postings.tell()
                            build_trigram_dictionary_count_dict(ngram_count_dict, term1, term2, term3, head3, tail3, freq3)
                        else:
                            # handle bigram
                            if term_or_doc_id2 not in doc_norm2:
                                values2 = [1 + math.log(i, 10) for i in doc_words2[term_or_doc_id2].values()]
                                norm_val2 = math.sqrt(sum(i ** 2 for i in values2))
                                doc_norm2[term_or_doc_id2] = norm_val2
                            bigram_posting.append(str(term_or_doc_id2) + '-' + str(dict_or_tf2))
                    
                    posting_str2 = " ".join(str(e) for e in bigram_posting) + " "

                    head2 = out_postings.tell()
                    out_postings.write(posting_str2)
                    freq2 = len(bigram_posting)
                    tail2 = out_postings.tell()
                    build_bigram_dictionary_count_dict(ngram_count_dict, term1, term2, head2, tail2, freq2)

                else:
                    # handle unigram
                    if term_or_doc_id1 not in doc_norm1:
                        values1 = [1 + math.log(i, 10) for i in doc_words1[term_or_doc_id1].values()]
                        norm_val1 = math.sqrt(sum(i ** 2 for i in values1))
                        doc_norm1[term_or_doc_id1] = norm_val1
                    unigram_posting.append(str(term_or_doc_id1) + '-' + str(dict_or_tf1))
            
            posting_str1 = " ".join(str(e) for e in unigram_posting) + " "

            head1 = out_postings.tell()
            out_postings.write(posting_str1)
            freq1 = len(unigram_posting)
            tail1 = out_postings.tell()
            build_unigram_dictionary_count_dict(ngram_count_dict, term1, head1, tail1, freq1)

    with open(output_file_dictionary, 'w') as out_dict:
        all_doc_ids.sort()
        ngram_count_dict['N'] = collection_size
        ngram_count_dict['DOC_NORM'] = (doc_norm1, doc_norm2, doc_norm3)
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
    write_ngram_dict_output(ngram_dictionary, ngram_dictionary_count_dict, output_ngram_dict, output_ngram_postings)
    write_meta_output(meta_dict, meta_count_dict, output_meta_dict, output_meta_postings)