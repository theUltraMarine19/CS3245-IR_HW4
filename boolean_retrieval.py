def get_postings(term, dictionary, postings):
    """
    This method returns the postings for a specific term from either dict1, dict2 or positional indexing.
    :param term: term of length 1, 2 or 3
    :param dictionary:
    :param postings:
    :return: postings for the given term
    """
    # TODO: term is still a string make sure it's a list or check for word count

    if (len(term) == 1)
        # check if its a single word
        # check if term in dictionary 1
        if term in dict1:
            # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
            # if not in dict 1, call synonyms and check for each of the top synonym if in dict 1
            # else get postings for term from dictionary 1 from postings.txt
            fp_postings.seek(dict1[term]['H'])
            postings_string = fp_postings.read(dict1[term]['T'] - dict1[term]['T'])
            postings_list = postings_string.split(' ')

    elif (len(term) == 2)
        # for terms of length 2, use the format of double indexing in dict'
        # check if term in dictionary 2
        if term[0] in dict1:
            if term[1] in dict1[term[0]]:
                # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                # TODO: since length 2, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word
                # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                # else get postings for term from dictionary 2 from postings.txt
                fp_postings.seek(dict1[term[0]][term[1]]['H'])
                postings_string = fp_postings.read(dict1[term[0]][term[1]]['T'] - dict1[term[0]][term[1]]['H'])
                postings_list = postings_string.split(' ')
    
    elif (len(term) == 3)
        # complicated
        # make use of positional indexes for fetching the postings
    else
        # throw an error

    # if successfully reaches here without error, return fetched postings list
    return postings_list

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

def order_by_size(term, dictionary, postings):
    """
    Evaluates the size of the posting list of a given expression (if existing in the term dictionary).
    :param term:
    :param dictionary:
    :param postings:
    :return: 0 - if not in the term dictionary
             document frequency of the term - if the term is present in the dictionary
    """
    res = 0
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
            return 0
        elif word2 not in dictionary[word1]:
            # TODO: check for synonyms
            return 0
        res = dictionary[word1][word2]
    elif len(expr_words) == 3:
        # TODO: use positional indexing
        res = 0
    else:
        print "Incorrect input"
    return res

# TODO: define get_synonyms as a new file or as a method

def bool_retrieve(query, dictionary, postings):
    """
    The main method for the boolean retrieval.
    The smallest sized list of postings should be merged first (orderBySize)
    :param query: a list of query terms
    :param dictionary:
    :param postings:
    :return: return the result of all relevant docIDs
    """