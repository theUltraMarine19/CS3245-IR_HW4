import json
import sys
import getopt
import re
import datetime

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

court_metadata = {"UK Military Court":0.5, 
                    "NSW Industrial Relations Commission":0.5,
                    "NSW Local Court":0.25, 
                    "UK House of Lords":1.0, 
                    "NSW Court of Criminal Appeal":0.75, 
                    "NSW Supreme Court":1.0,
                    "NSW Land and Environment Court":0.5,
                    "Industrial Relations Court of Australia":0.25,
                    "NSW Court of Appeal":0.75, 
                    "SG Family Court":0.5,
                    "SG Privy Council":0.25, 
                    "NSW District Court":0.5,
                    "NSW Administrative Decisions Tribunal (Trial)":0.25, 
                    "NSW Industrial Court":0.25, 
                    "High Court of Australia":0.75,
                    "Singapore International Commercial Court":0.75, 
                    "CA Supreme Court":1.0, 
                    "SG High Court": 0.75, 
                    "SG District Court":0.5, 
                    "NSW Children's Court":0.5, 
                    "UK Supreme Court": 1.0, 
                    "SG Magistrates' Court": 0.5,
                    "UK High Court": 0.75, 
                    "HK High Court": 0.75, 
                    "NSW Medical Tribunal": 0.25,
                    "Federal Court of Australia": 1.0,
                    "HK Court of First Instance": 0.5,
                    "UK Court of Appeal": 1.0,
                    "NSW Civil and Administrative Tribunal": 0.25,
                    "SG Court of Appeal": 1.0, 
                    "UK Crown Court": 0.75}


def get_date_factor(date_string):
    split_string = date_string.split(" ")
    date = split_string[0]
    time = split_string[1]

    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[3]

    year = int(year)
    curr_year = int(datetime.now().year)

    if(year >= curr_year - 10):
        return 1.0
    elif(year >= curr_year - 20):
        return 0.75
    elif(year >= curr_year - 40):
        return 0.50
    else:
        0.25

def load_dict_file(dict_file):
    with open(dict_file, 'r') as dictionary_f:
        return json.load(dictionary_f)

def load_meta_dict_file(dict_file):
    with open(dict_file, 'r') as dictionary_f:
        return json.load(dictionary_f)

def zones_metadata(doc_id_score_list, dictionary):
    res = []
    court_name_factor = 0.8
    date_factor = 0.2
    for (doc_id, score) in doc_id_score_list:
        court_name = dictionary['court'][doc_id]
        court_score = court_metadata.get(court_name, 0)

        date = dictionary['date_posted'][doc_id]
        date_score = get_date_factor(date)

        final_score_factor = court_name_factor*court_score + date_factor*date_score

        res.append((doc_id, score*final_score_factor))
    return res

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
    fp_postings = open(postings_file, 'r')
    term_dictionary = load_dict_file(dictionary_file)

    metadata_dictionary = load_meta_dict_file("metadict.txt")
    
    with open(file_of_queries, 'r') as fp:
        query = fp.readlines()
        if "AND" in query[0] or "\"" in query[0][0].strip():
            # call boolean retrieval -> e.g boolRetriev(query.split('AND'))
            res = br.bool_retrieve(query[0].split("AND"), term_dictionary, fp_postings)
        else:
            # call freetext retrieval -> e.g freetextRetriev(query.split(' '))
            separate_terms = re.findall(r'(?P<q_marks>\"(.*?)\")|(?P<s_word>\w+)', query[0])
            terms = []
            for b, q, s in separate_terms:
                if b:
                    terms.append(b.replace('"', ''))
                elif q:
                    terms.append(q)
                elif s:
                    terms.append(s)
            res = fr.freetext_retrieve(terms, term_dictionary, fp_postings)
            # res = zones_metadata(res, metadata_dictionary)
            res = [x[0] for x in res]

    with open(file_of_output, 'w') as out:
        out_str = str()
        out_str += ' '.join(str(el) for el in res) + '\n'
        out.write(out_str[:-1])  # removes the last '\n'


if __name__ == "__main__":
    main()