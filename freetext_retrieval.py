def build_vec_from_term(term, dict1, dict2, postings):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param dict1:
    :param dict2:
    :param postings:
    :return: the (?normalized) vector for the term
    """


def build_phrasal_vec(phrasal_term, dict1, dict2, postings):
    """
    New York university : Is this doc relevant? -> I went to York university at New York
    Compicated maths, think about how to make it comp
    :param term:
    :param dict1:
    :param dict2:
    :param postings:
    :return:
    """

# TODO: define getSynonyms as a new file or as a method


def freetext_retrieve(query, dict1, dict2, postings):
    """
    The main method for the free text retrieval.
    :param query: a list of query terms
    :param dict1:
    :param dict2:
    :param postings:
    :return: return the result of all relevant docIDs in decreasing order of priority using a heap (heapq module)
    """