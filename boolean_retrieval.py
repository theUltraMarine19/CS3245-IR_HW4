import sys
def get_postings(term, dictionary, fp_postings):
    """
    This method returns the postings for a specific term from either dict1, dict2 or positional indexing.
    :param term: term of length 1, 2 or 3
    :param dictionary:
    :param fp_postings:
    :return: postings for the given term
    """
    # TODO: term is still a string make sure it's a list or check for word count

    if len(term) == 1:
        # check if its a single word
        # check if term in dictionary 1
        if term in dictionary:
            # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
            # if not in dict 1, call synonyms and check for each of the top synonym if in dict 1
            # else get postings for term from dictionary 1 from postings.txt
            fp_postings.seek(dictionary[term]['H'])
            postings_string = fp_postings.read(dictionary[term]['T'] - dictionary[term]['H'])
            postings_list = postings_string.split()

    elif len(term) == 2:
        # for terms of length 2, use the format of double indexing in dict'
        # check if term in dictionary 2
        if term[0] in dictionary:
            if term[1] in dictionary[term[0]]:
                # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                # TODO: since length 2, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word
                # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                # else get postings for term from dictionary 2 from postings.txt
                fp_postings.seek(dictionary[term[0]][term[1]]['H'])
                postings_string = fp_postings.read(dictionary[term[0]][term[1]]['T'] - dictionary[term[0]][term[1]]['H'])
                postings_list = postings_string.split()
    
    elif len(term) == 3:
        if term[0] in dictionary:
            if term[1] in dictionary[term[0]]:
                if term[2] in dictionary[term[0]][term[1]]:
                    # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                    # TODO: since length 3, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word etc.
                    # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                    # else get postings for term from dictionary 2 from postings.txt
                    fp_postings.seek(dictionary[term[0]][term[1]][term[2]]['H'])
                    postings_string = fp_postings.read(dictionary[term[0]][term[1]][term[2]]['T'] - dictionary[term[0]][term[1]][term[2]]['H'])
                    postings_list = postings_string.split()
        # OR second approach:
        # complicated
        # make use of positional indexes for fetching the postings
    else:
        print "ERROR: phrase contains more than 3 terms"
        sys.exit(2)
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

def order_by_size(term_list, dictionary, fp_postings):
    """
    Evaluates the size of the posting list of a given expression (if existing in the term dictionary).
    :param term_list:
    :param dictionary:
    :param fp_postings:
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
                return 0
            elif word2 not in dictionary[word1]:
                # TODO: check for synonyms
                return 0
            res = dictionary[word1][word2]['f']
        elif len(expr_words) == 3:
            word1 = expr_words[0]
            word2 = expr_words[1]
            word3 = expr_words[2]
            if word1 not in dictionary:
                # TODO: check for synonyms
                return 0
            elif word2 not in dictionary[word1]:
                # TODO: check for synonyms
                return 0
            elif word3 not in dictionary[word1][word2]:
                return 0
            # Approach 2 will be:
            # TODO: use positional indexing
            res = dictionary[word1][word2][word3]['f']
        else:
            print "Incorrect input"
            return
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