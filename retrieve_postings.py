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
            synonyms.append(l.name())

    return synonyms


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
        if term[0] in dictionary:
            # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
            # if not in dict 1, call synonyms and check for each of the top synonym if in dict 1
            # else get postings for term from dictionary 1 from postings.txt

            synonyms_word1 = get_synonyms(term[0])
            synonyms_word2 = get_synonyms(term[1])

            fp_postings.seek(dictionary[term[0]]['H'])
            postings_string = fp_postings.read(dictionary[term[0]]['T'] - dictionary[term[0]]['H'])
            postings_list = postings_string.split()

    elif len(term) == 2:
        # for terms of length 2, use the format of double indexing in dict'
        # check if term in dictionary 2
        if term[0] in dictionary:
            if term[1] in dictionary:
                # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                # TODO: since length 2, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word
                # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                # else get postings for term from dictionary 2 from postings.txt
                # TODO: change to positional indexing
                fp_postings.seek(dictionary[term[0]][term[1]]['H'])
                postings_string = fp_postings.read(
                    dictionary[term[0]][term[1]]['T'] - dictionary[term[0]][term[1]]['H'])
                postings_list = postings_string.split()

    elif len(term) == 3:
        if term[0] in dictionary:
            if term[1] in dictionary[term[0]]:
                if term[2] in dictionary[term[0]][term[1]]:
                    # TODO: if we don't have enough docIDs in postings for a given term, check more synonyms
                    # TODO: since length 3, fist check synonyms for the first word, if not enough docIDs, check synonyms for 2. word etc.
                    # if not in dict 2, call synonyms and check for each of the top synonym if in dict 2
                    # else get postings for term from dictionary 2 from postings.txt
                    # TODO: change to positional indexing
                    fp_postings.seek(dictionary[term[0]][term[1]][term[2]]['H'])
                    postings_string = fp_postings.read(
                        dictionary[term[0]][term[1]][term[2]]['T'] - dictionary[term[0]][term[1]][term[2]]['H'])
                    postings_list = postings_string.split()
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