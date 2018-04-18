import json
import sys
import getopt
import math
import re
from nltk.tokenize import word_tokenize
from operator import mul
from nltk.stem.porter import PorterStemmer

import boolean_retrieval as br
import freetext_retrieval as fr

# params:
# -d posdict.txt -p pospostings.txt -q queries.txt -o output.txt

'''
======================
==== Assignment 4 ====
======================

- A0179092W-A0175111U-A0179365N-A0179262X
'''

term_dict = {}

def load_dict_file(dict_file):
    with open(dict_file, 'r') as dictionary_f:
        return json.load(dictionary_f)


def usage():
    print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file is None or postings_file is None or file_of_queries is None or file_of_output is None :
    usage()
    sys.exit(2)


def main():
    #TODO: read query from file
    fp_postings = open(postings_file, 'r')
    term_dict = load_dict_file(dictionary_file)
    
    with open(file_of_queries, 'r') as fp:
        queries = fp.readlines()
        for query in queries:
            if "AND" in query:
                # call boolean retrieval -> e.g boolRetriev(query.split('AND'))
                res = br.bool_retrieve(query.split("AND"), term_dict, fp_postings) 
                print "bool " + res
            else:
                # call freetext retrieval -> e.g freetextRetriev(query.split(' '))
                separate_terms = re.findall(r'(?P<q_marks>\"(.*?)\")|(?P<s_word>\w+)', query)
                terms = []
                for b, q, s in separate_terms:
                    if b:
                        terms.append(b.replace('"', ''))
                    elif q:
                        terms.append(q)
                    elif s:
                        terms.append(s)
                res = fr.freetext_retrieve(terms, term_dict, fp_postings)
                print res



if __name__ == "__main__":
    main()