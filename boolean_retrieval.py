from retrieve_postings import get_postings

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

def order_by_size(term_list, dictionary):
    """
    Evaluates the size of the posting list of a given expression (if existing in the term dictionary).
    :param term_list:
    :param dictionary:
    :return: 0 - if not in the term dictionary
             document frequency of the term - if the term is present in the dictionary
    """
    smallest_index = 0
    smallest_f = 18000
    cur_index = 0
    for term in term_list:
        term = term.strip()
        expr_words = term.split()
        if len(expr_words) == 1:
            if term not in dictionary:
                # TODO: check for synonyms
                return 0
            res = dictionary[term]['f']
        elif len(expr_words) == 2:
            word1 = expr_words[0]
            word2 = expr_words[1]
            if word1 not in dictionary:
                # TODO: check for synonyms
                synonym = word1
                res = dictionary[synonym]['f']
                #return 0
            else:
                # TODO: use positional indexing + check for synonyms
                res = dictionary[word1]['f']
                #return 0
        elif len(expr_words) == 3:
            word1 = expr_words[0]
            word2 = expr_words[1]
            word3 = expr_words[2]
            if word1 not in dictionary:
                # TODO: check for synonyms
                synonym = word1
                res = dictionary[synonym]['f']
                #return 0
            else:
                # TODO: use positional indexing + check for synonyms
                res = dictionary[word1]['f']
                #return 0
        else:
            print "Incorrect input"
            return 0
        # used to sort the boolean query by size for optimization purposes
        if res < smallest_f:
            smallest_index = cur_index
        cur_index += 1
    res_list = term_list
    if smallest_index != 0:
        tmp = res_list[smallest_index]
        res_list[smallest_index] = res_list[0]
        res_list[0] = tmp
    return res_list

# TODO: define get_synonyms as a new file or as a method

def bool_retrieve(query, dictionary, fp_postings):
    """
    The main method for the boolean retrieval.
    The smallest sized list of postings should be merged first (orderBySize)
    :param query: a list of query terms
    :param dictionary:
    :param fp_postings:
    :return: return the result of all relevant docIDs
    """
    res = []
    for term in query:
        term_postings = get_postings(term.split(), dictionary, fp_postings)
        res = merge_lists(res, term_postings)
    return res
