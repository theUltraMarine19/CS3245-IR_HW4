import sys
from nltk.corpus import wordnet


def get_synonyms(term):
    """
    This method returns the synonyms of a given term
    :param term: a single word
    :return: all synonyms of the term
    """
    term_list = term.split()
    if len(term_list) > 1:
        print "ERROR: Passing more than one word to gen_synonyms"
        return -1

    # get synonyms
    syns_word = wordnet.synsets(term)
    synonyms = []
    for syn in syns_word:
        for l in syn.lemmas():
            # TODO: Check if that's fine
            if l.name() not in synonyms:
                synonyms.append(l.name())

    return synonyms


def positional_intersect(l1, l2):
    """
    Create a list of all elements that are common for both lists.
    :param l1: the first list that is part of the merge
    :param l2: the second list that is part of the merge
    :return: the result after applying the AND merge on the two lists
    """
    l1_len = len(l1.split(' '))
    l2_len = len(l2.split(' '))
    ans = []

    if l1_len == 0 or l2_len == 0:
        return ans
    elif (l1_len == 1 and l1.split(' ')[0] == '') or (l2_len == 1 and l2.split(' ')[0] == ''):
        return ans

    p1 = p2 = 0
    while p1 < l1_len and p2 < l2_len:
        l1_doc_id = l1.split(' ')[p1].split('-')[0]
        l2_doc_id = l2.split(' ')[p2].split('-')[0]

        if l1_doc_id == l2_doc_id:

            pos_ans = []
            pp1 = pp2 = 0

            pl1_len = len(l1.split(' ')[p1].split('-')[1:])
            pl2_len = len(l2.split(' ')[p2].split('-')[1:])

            while pp1 < pl1_len:
                while pp2 < pl2_len:

                    pos1 = l1.split(' ')[p1].split('-')[pp1 + 1]
                    pos2 = l2.split(' ')[p2].split('-')[pp2 + 1]
                    if (pos2 - pos1) == 1:
                        pos_ans(pos2)
                    elif pos2 > pos1:
                        break
                    pp2 += 1

                while len(pos_ans) != 0 and (pos_ans[0] - pos1) != 1:
                    pos_ans = pos_ans[1:]

                for ps in pos_ans:
                    ans.append((l1_doc_id, (pos1, ps)))

                pp1 += 1

            # ans.append(l1_doc_id)
            p1 += 1
            p2 += 1
        elif l1_doc_id < l2_doc_id:
            p1 += 1
        else:
            p2 += 1
    return ans


def get_postings(term, dictionary, fp_postings):
    """
    This method returns the postings for a specific term from either dict1, dict2 or positional indexing.
    :param term: term of length 1, 2 or 3
    :param dictionary:
    :param fp_postings:
    :return: postings for the given term
    """
    if type(term) != list:
        term_list = term.split()
    else:
        term_list = term
    # TODO: term is still a string make sure it's a list or check for word count
    if len(term_list) == 1:
        # check if its a single word
        # check if term in dictionary 1
        if term_list[0] in dictionary:
            # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
            # if not in dict 1, call synonyms and check for each of the top synonym if in dict 1
            # else get postings for term from dictionary 1 from postings.txt

            fp_postings.seek(dictionary[term_list[0]]['H'])
            postings_string = fp_postings.read(dictionary[term_list[0]]['T'] - dictionary[term_list[0]]['H'])
            postings_list = postings_string.split()
            postings_list = [doc_id_position_string.split("-") for doc_id_position_string in postings_list]
            postings_list = [(doc_id_position_list[0], len(doc_id_position_list) - 1) for doc_id_position_list in
                             postings_list]

    elif len(term_list) == 2:
        # for terms of length 2, use the format of double indexing in dict'
        # check if term in dictionary 2
        if term_list[0] in dictionary:
            if term_list[1] in dictionary:
                # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                # TODO: since length 2, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word
                # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                # else get postings for term from dictionary 2 from postings.txt
                # TODO: change to positional indexing
                synonyms_word1 = get_synonyms(term_list[0])
                synonyms_word2 = get_synonyms(term_list[1])

                fp_postings.seek(dictionary[term[0]]['H'])
                postings1_str = fp_postings.read(dictionary[term[0]]['T'] - dictionary[term[0]]['H'])
                fp_postings.seek(dictionary[term[1]]['H'])
                postings2_str = fp_postings.read(dictionary[term[1]]['T'] - dictionary[term[0]]['H'])
                postings_string = positional_intersect(postings1_str, postings2_str)
                
                postings_list = [x[0] for x in postings_string]

    elif len(term_list) == 3:
        if term_list[0] in dictionary:
            if term_list[1] in dictionary:
                if term_list[2] in dictionary:
                
                    # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                    # TODO: since length 3, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word etc.
                    # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                    # else get postings for term from dictionary 2 from postings.txt
                    fp_postings.seek(dictionary[term[0]]['H'])
                    postings1_string = fp_postings.read(dictionary[term[0]]['T'] - dictionary[term[0]]['H'])
                    fp_postings.seek(dictionary[term[1]]['H'])
                    postings2_string = fp_postings.read(dictionary[term[1]]['T'] - dictionary[term[1]]['H'])
                    fp_postings.seek(dictionary[term[1]]['H'])
                    postings3_string = fp_postings.read(dictionary[term[2]]['T'] - dictionary[term[2]]['H'])
                    postings12_list = positional_intersect(postings1_string, postings2_string)
                    postings23_list = positional_intersect(postings2_string, postings3_string)
                    final_postings = []
                    for tup1 in postings12_list:
                        for tup2 in postings23_list:
                            if tup1[0] == tup2[0] and tup1[1][1] == tup2[1][0]:
                                final_postings.append(tup1[0])

                    postings_list = final_postings            
                    # OR second approach:
                    # complicated
                    # make use of positional indexes for fetching the postings
    else:
        print "ERROR: phrase contains more than 3 terms"
        sys.exit(2)
    # if successfully reaches here without error, return fetched postings list

    postings_list_tuple = []
    for e in postings_list:
        e_list = e.split('-')
        tf = len(e_list) - 1
        # if boolean retrieval is called with phrase, then add positional indexing at the end
        postings_list_tuple.append((int(e_list[0]), tf))

    return postings_list_tuple


