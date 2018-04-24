import re
from nltk.corpus import wordnet

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


def get_synonyms(term):
    """
    This method returns the synonyms of a given term
    :param term: a single word
    :return: all synonyms of the term
    """
    term_list = term.split()
    if len(term_list) > 1:
        print "ERROR: Passing more than one word to get_synonyms"
        return -1

    # get synonyms
    syns_word = wordnet.synsets(term)
    synonyms = []
    for syn in syns_word:
        for l in syn.lemmas():
            if l.name() not in synonyms:
                synonyms.append(l.name())
    return synonyms


def handle_synonyms(term_list, dictionary, fp_postings):
    all_synonyms = []
    for i in term_list:
        synonyms = get_synonyms(i)
        synonyms = [ps.stem((re.sub(r'[^a-zA-Z0-9]', '', str(x))).lower()) for x in synonyms]
        synonyms = [x for x in synonyms if x in dictionary]
        if synonyms:
            for syn in synonyms[1:5]:
                if len(all_synonyms) >= 5:
                    return all_synonyms
                elif syn in dictionary:
                    fp_postings.seek(dictionary[syn]['H'])
                    postings_string = fp_postings.read(dictionary[syn]['T'] - dictionary[syn]['H'])
                    all_synonyms.extend(postings_string.split())

    return all_synonyms


def handle_synonyms_unigram(term_list, dictionary, fp_postings):
    all_synonyms = ''
    for i in term_list:
        synonyms = get_synonyms(i)
        synonyms = [ps.stem((re.sub(r'[^a-zA-Z0-9]', '', str(x))).lower()) for x in synonyms]
        new_term = ps.stem((re.sub(r'[^a-zA-Z0-9]', '', str(i))).lower())
        synonyms = [x for x in synonyms if x in dictionary]
        for syn in synonyms:
            if(syn == new_term):
                continue
            else:
                fp_postings.seek(dictionary[syn]['H'])
                postings_string = fp_postings.read(dictionary[syn]['T'] - dictionary[syn]['H'])
                all_synonyms += ' ' + postings_string
                break
    return all_synonyms.strip()