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


'''
======================
==== Assignment 4 ====
======================

- A0179092W-A0175111U-A0179365N
'''

term_dict1 = dict()
term_dict2 = dict()
fp_postings = open(postingsFile, 'r')

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
    query = ''
    if "AND" in query:
        # call boolean retrieval -> e.g boolRetriev(query.split('AND'))
        br.bool_retrieve(query.split("AND"), term_dict1, term_dict2, fp_postings)
    else:
        # call freetext retrieval -> e.g freetextRetriev(query.split(' '))
        # TODO: change with regex! -> separate by space only if no " " (phrases) in between)
        fr.freetext_retrieve(query.split(), term_dict1, term_dict2, fp_postings)

if __name__ == "__main__":
    main()