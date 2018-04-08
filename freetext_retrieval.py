import re
from retrieve_postings import get_postings
from nltk.stem.porter import PorterStemmer
import math

ps = PorterStemmer()

def tf_val_for_term(term, occurences, dictionary, fp_postings):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param dictionary:
    :param fp_postings:
    :return: the (?normalized) vector for the term
    """
    return []


def tf_val_for_phrase(phrasal_term, occurences, dictionary, fp_postings):
    """
    New York university : Is this doc relevant? -> I went to York university at New York
    Compicated maths, think about how to make it comp
    :param phrasal_term:
    :param dictionary:
    :param fp_postings:
    :return:
    """
    return []

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
    doc_vecs = []
    res = []
    stemmed_query = []
    for term in query:
        term = re.sub(r'[^a-zA-Z0-9]', '', str(term))
        term = ps.stem(term.lower())
        stemmed_query.append(term)
    # remove words appearing more than once because we count them in the t_f computation below
    stemmed_query_set = set(stemmed_query)
    for term in stemmed_query_set:
        string_term = term.split()
        # don't check if term is in dictionary, because it will try to find synonyms in build_vec methods
        if len(string_term) == 1:
            # TODO: important, return handled term
            val , new_term = tf_val_for_term(term, occurences, dictionary, fp_postings)
            query_vec.append(vec)
        elif len(string_term) <= 3:
            # TODO: important, return handled term
            val, new_term = tf_val_for_phrase(term, occurences, dictionary, fp_postings)
            query_vec.append(vec)
        else:
            print "Incorrect input"
            break

        cur_docs = get_postings(new_term)
        for doc, tf in cur_docs:
            norm = dictionary['DOC_NORM'][str(doc)]
            t_f = 1 + math.log(tf, 10)
            val = t_f / norm
            if doc in doc_vecs:
                doc_vecs[doc][new_term] = val
            else:
                doc_vecs[doc] = {new_term: val}
    # TODO: Discuss if this approach is fine with all team members, basically the same as HW3
    # If the approach is approved, finish!
    return res
