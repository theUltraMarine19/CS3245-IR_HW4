import re
from retrieve_postings import get_postings
from nltk.stem.porter import PorterStemmer
import math
from operator import mul

ps = PorterStemmer()


def compute_log_tf(tf):
    """
    Calcluates the the logarithmic value of the given term frequency
    :param tf: term frequency
    :return: type float, the logarithmic value of the term frequency
    """
    # formula: 1 + log_10(term frequency)
    return 1.0 + math.log10(tf) if tf != 0 else 0.0


def tf_val_for_term(term, occurrences, dictionary):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param occurrences:
    :param dictionary:
    :return: the (?normalized) vector for the term,
    """
    if term not in dictionary:
        #TODO: chenage to synonyms
        return (0, None)
    log_tf = 1.0 + math.log10(occurrences) if occurrences != 0 else 0.0
    log_idf = math.log10(float(dictionary['N'])/float(dictionary[term]['F']))
    # TODO: synonyms, return term
    return log_tf * log_idf, [term]


def tf_val_for_phrase(phrasal_term, occurrences, dictionary):
    """
    New York university : Is this doc relevant? -> I went to York university at New York
    Compicated maths, think about how to make it comp
    :param phrasal_term:
    :param occurrences:
    :param dictionary:
    :return:
    """
    if len(phrasal_term) == 2:
        term1 = phrasal_term[0]
        term2 = phrasal_term[1]
        if term1 not in dictionary:
            return 0, None
        if term2 not in dictionary[term1]:
            return 0, None
        log_tf = 1.0 + math.log10(occurrences) if occurrences != 0 else 0.0
        log_idf = math.log10(float(dictionary['N'])/float(dictionary[term1][term2]['F']))
    else:
        term1 = phrasal_term[0]
        term2 = phrasal_term[1]
        term3 = phrasal_term[2]
        if term1 not in dictionary:
            return 0, None
        if term2 not in dictionary[term1]:
            return 0, None
        if term3 not in dictionary[term1][term2]:
            return 0, None
        log_tf = 1.0 + math.log10(occurrences) if occurrences != 0 else 0.0
        log_idf = math.log10(float(dictionary['N'])/float(dictionary[term1][term2][term3]['F']))

    return log_tf * log_idf, phrasal_term

# TODO: define getSynonyms as a new file or as a method


def freetext_retrieve(query, dictionary, fp_postings):
    """
    The main method for the free text retrieval.
    :param query: a list of query terms
    :param dictionary:
    :param fp_postings:
    :return: return the result of all relevant docIDs in decreasing order of priority using a heap (heapq module)
    """
    query_vec = []
    doc_vecs = {}
    stemmed_query = []
    for term in query:
        term = re.sub(r'[^a-zA-Z0-9]', '', str(term))
        term = ps.stem(term.lower())
        stemmed_query.append(term)
    # remove words appearing more than once because we count them in the t_f computation below
    stemmed_query_set = set(stemmed_query)

    for term in stemmed_query_set:
        #TODO: Oscar: var naming: string_term is a list, not string
        string_term = term.split()
        # don't check if term is in dictionary, because it will try to find synonyms in build_vec methods
        if len(string_term) == 1:
            # TODO: important, return handled term
            val, new_term = tf_val_for_term(term, stemmed_query.count(term), dictionary, fp_postings)
            query_vec.append(val)
        elif len(string_term) <= 3:
            # TODO: important, return handled term
            val, new_term = tf_val_for_phrase(string_term, stemmed_query.count(term), dictionary, fp_postings)
            query_vec.append(val)
        else:
            print "Incorrect input"
            break

        if new_term is None:
            continue

        cur_docs = get_postings(new_term, dictionary, fp_postings)
        for (doc, tf) in cur_docs:
            if len(new_term) == 1:
                norm = dictionary['DOC_NORM'][0][str(doc)]
            elif len(new_term) == 2:
                norm = dictionary['DOC_NORM'][1][str(doc)]
            else:
                norm = dictionary['DOC_NORM'][2][str(doc)]
            t_f = 1 + math.log(tf, 10) if tf != 0 else 0.0
            val = t_f / norm
            new_term_string = ' '.join(new_term)
            if doc in doc_vecs:
                doc_vecs[doc][new_term_string] = val
            else:
                doc_vecs[doc] = {new_term_string: val}

    # Fill all document vectors with 0 for the query words they don't contain
    norm_doc_vects = dict()
    for word in stemmed_query_set:
        if word in dictionary:
            for doc, dic in doc_vecs.iteritems():
                if word in dic:
                    # if doc in the dict, append the next normalized value
                    if doc in norm_doc_vects:
                        norm_doc_vects[doc].append(dic[word])
                    # if doc not in the dict of documents
                    else:
                        norm_doc_vects[doc] = [dic[word]]
                # if the word does not appear in the document
                else:
                    if doc in norm_doc_vects:
                        norm_doc_vects[doc].append(0)
                    else:
                        norm_doc_vects[doc] = [0]

    print query_vec
    # TODO - get divison by zero error here with phrasal queries, need to check
    q_vec_norm = math.sqrt(sum(i ** 2 for i in query_vec))
    q_vec_norm = [x / q_vec_norm for x in query_vec]
    res_vect = []
    sorted_rel_docs = sorted(norm_doc_vects.keys())

    for doc in sorted_rel_docs:
        doc_vec = norm_doc_vects[doc]
        similarity = sum(map(mul, q_vec_norm, doc_vec))
        res_vect.append((doc, round(similarity, 15)))
    # python sort method is stable and thus guarantee that docIDs with the same similarities
    # will remain in increasing order since they were inserted in the res_vect list in that order
    res_vect.sort(key=lambda x: x[1], reverse=True)
    res = [i[0] for i in res_vect]

    return res
