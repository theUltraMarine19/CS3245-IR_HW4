def build_vec_from_term(term, dictionary, fp_postings):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param dictionary:
    :param fp_postings:
    :return: the (?normalized) vector for the term
    """


def build_phrasal_vec(phrasal_term, dictionary, fp_postings):
    """
    New York university : Is this doc relevant? -> I went to York university at New York
    Compicated maths, think about how to make it comp
    :param phrasal_term:
    :param dictionary:
    :param fp_postings:
    :return:
    """

# TODO: define getSynonyms as a new file or as a method


def freetext_retrieve(query, dictionary, fp_postings):
    """
    The main method for the free text retrieval.
    :param query: a list of query terms
    :param dictionary:
    :param fp_postings:
    :return: return the result of all relevant docIDs in decreasing order of priority using a heap (heapq module)
    """
    res = []
    for term in query:
        term_postings = get_postings(term.split(), dictionary, fp_postings)
        res = merge_lists(res, term_postings)
    return res
