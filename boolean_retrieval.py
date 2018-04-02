def get_postings(term, dict1, dict2, postings):
    """
    This method returns the postings for a specific term from either dict1, dict2 or positional indexing.
    :param term: term of length 1, 2 or 3
    :param dict1:
    :param dict2:
    :param postings:
    :return: postings for the given term
    """
    # TODO: term is still a string make sure it's a list or check for word count
    if len(term) == 1:
        # check if term in dictionary 1
        # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
        # if not in dict 1, call synonyms and check for each of the top synonym if in dict 1
        # else get postings for term from dictionary 1 from postings.txt
    elif len(term) == 2:
        # check if term in dictionary 2
        # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
        # TODO: since length 2, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word
        # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
        # else get postings for term from dictionary 2 from postings.txt
    elif len(term) == 3:
        # complicated
    else:
        # throw an error

def merge_lists(l1, l2):
    """
    Create a list of all elements that are common for both lists.
    :param l1: the first list that is part of the merge
    :param l2: the second list that is part of the merge
    :return: the result after applying the AND merge on the two lists
    """
    l1_len = len(l1)
    l2_len = len(l2)
    ans = []
    if l1_len == 0 or l2_len == 0:
        return ans
    p1 = p2 = 0
    while p1 < l1_len and p2 < l2_len:
        l1_doc_id = l1[p1]
        l2_doc_id = l2[p2]
        if l1_doc_id == l2_doc_id:
            ans.append(l1_doc_id)
            p1 += 1
            p2 += 1
        elif l1_doc_id < l2_doc_id:
            p1 += 1
        else:
            p2 += 1
    return ans


# TODO: Can we have boolean retrieval and free text in one query

def order_by_size(query, dict1, dict2, postings):
    """

    :param query:
    :param dict1:
    :param dict2:
    :param postings:
    :return:
    """

# TODO: define get_synonyms as a new file or as a method

def bool_retrieve(query, dict1, dict2, postings):
    """
    The main method for the boolean retrieval.
    The smallest sized list of postings should be merged first (orderBySize)
    :param query: a list of query terms
    :param dict1:
    :param dict2:
    :param postings:
    :return: return the result of all relevant docIDs
    """