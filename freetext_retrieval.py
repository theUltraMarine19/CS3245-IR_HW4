def buildVecFromTerm(term, dict1, dict2, postings):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param dict1:
    :param dict2:
    :param postings:
    :return: the (?normalized) vector for the term
    """


def buildPhrasalVec(term, dict1, dict2, postings):
    """

    :param term:
    :param dict1:
    :param dict2:
    :param postings:
    :return:
    """


def calculateRelevance(listOfTerms):
    """

    :param listOfTerms:
    :return:
    """



def freetextRetrieve(query, dict1, dict2, postings):
    """
    The main method for the free text retrieval.
    :param query: a list of query terms
    :param dict1:
    :param dict2:
    :param postings:
    :return: return the result of all relevant docIDs in decreasing order of priority
    """