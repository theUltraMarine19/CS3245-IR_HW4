import re
from retrieve_postings import get_postings
from nltk.stem.porter import PorterStemmer
import math
from operator import mul

ps = PorterStemmer()

def tf_val_for_term(term, occurrences, dictionary):
    """
    In this method a tf-idf vector for the term is build as in HW3.
    Need to handle synonyms for the terms that are not part of dict1 or dict 2.
    :param term:
    :param occurrences:
    :param dictionary:
    :return: the (?normalized) vector for the term,
    """
    if term not in dictionary:
        #TODO: chenage to synonyms
        return (0, None)
    log_tf = 1.0 + math.log10(occurrences) if occurrences != 0 else 0.0
    log_idf = math.log10(float(dictionary['N'])/float(dictionary[term]['F']))
    # TODO: synonyms, return term
    return log_tf * log_idf, [term]

def get_cosine_similarity(query_vec, norm_doc_vects, flag):
    res_vect = []
    sorted_rel_docs = sorted(norm_doc_vects.keys())

    for doc in sorted_rel_docs:
        doc_vec = norm_doc_vects[doc]
        similarity = sum(map(mul, query_vec, doc_vec))
        res_vect.append((doc, round(similarity, 15)))
    # python sort method is stable and thus guarantee that docIDs with the same similarities
    # will remain in increasing order since they were inserted in the res_vect list in that order
    if (flag == True):
        res_vect.sort(key=lambda x: x[1], reverse=True)
    return res_vect


def get_expanded_query(query_vec, norm_doc_vects, res_vect):
    rf_threshold = 0.3
    num_total = len(norm_doc_vects)
    num_relevant = int(rf_threshold * num_total)
    num_irrelevant = num_total - num_relevant
    centroid_relevant = [0.0 for i in range(len(query_vec))]
    centroid_irrelevant = [0.0 for i in range(len(query_vec))]

    alpha = 1
    beta = 0.8
    #TODO modern rocchio uses gamma = 0, check if it's needed
    gamma = 0.1

    for i in range(num_relevant):
        doc_id_to_get = res_vect[i][0]
        doc_vec = norm_doc_vects[doc_id_to_get]
        centroid_relevant = [x + y for x, y in zip(centroid_relevant, doc_vec)]

    for i in range(num_relevant, num_total):
        doc_id_to_get = res_vect[i][0]
        doc_vec = norm_doc_vects[doc_id_to_get]
        centroid_irrelevant = [x + y for x, y in zip(centroid_irrelevant, doc_vec)]

    expanded_query_vec = [alpha * x + beta * y / num_relevant + gamma * z / num_irrelevant for x, y, z in
                          zip(query_vec, centroid_relevant, centroid_irrelevant)]

    return expanded_query_vec


# TODO: define getSynonyms as a new file or as a method
def freetext_retrieve(query, dictionary, fp_postings, flag):
    """
    The main method for the free text retrieval.
    :param query: a list of query terms
    :param dictionary:
    :param fp_postings:
    :return: return the result of all relevant docIDs in decreasing order of priority using a heap (heapq module)
    """
    query_vec = []
    doc_vecs = {}
    stemmed_query = []
    for term in query:
        term = re.sub(r'[^a-zA-Z0-9]', '', str(term))
        term = ps.stem(term.lower())
        stemmed_query.append(term)
    # remove words appearing more than once because we count them in the t_f computation below
    stemmed_query_set = set(stemmed_query)

    for term in stemmed_query_set:
        #TODO: Oscar: var naming: string_term is a list, not string
        string_term = term.split()
        # don't check if term is in dictionary, because it will try to find synonyms in build_vec methods
        if len(string_term) == 1:
            # TODO: important, return handled term
            val, new_term = tf_val_for_term(term, stemmed_query.count(term), dictionary)
            if (new_term is not None):
                query_vec.append(val)
        else:
            print "Incorrect input"
            break

        if new_term is None:
            continue

        cur_docs = get_postings(new_term, dictionary, fp_postings)
        cur_docs = [(int(x[0]), x[1]) for x in cur_docs]
        for (doc, tf) in cur_docs:
            norm = dictionary['DOC_NORM'][str(doc)]
            t_f = 1 + math.log(tf, 10) if tf != 0 else 0.0
            val = t_f / norm
            new_term_string = new_term[0]
            if doc in doc_vecs:
                doc_vecs[doc][new_term_string] = val
            else:
                doc_vecs[doc] = {new_term_string: val}

    # Fill all document vectors with 0 for the query words they don't contain
    norm_doc_vects = {}
    for word in stemmed_query_set:
        if word in dictionary:
            for doc, dic in doc_vecs.iteritems():
                if word in dic:
                    # if doc in the dict, append the next normalized value
                    if doc in norm_doc_vects:
                        norm_doc_vects[doc].append(dic[word])
                    # if doc not in the dict of documents
                    else:
                        norm_doc_vects[doc] = [dic[word]]
                # if the word does not appear in the document
                else:
                    if doc in norm_doc_vects:
                        norm_doc_vects[doc].append(0)
                    else:
                        norm_doc_vects[doc] = [0]

    res_vect = get_cosine_similarity(query_vec, norm_doc_vects, flag)
    # expanded_query_vec = get_expanded_query(query_vec, norm_doc_vects, res_vect)
    # res_vect = get_cosine_similarity(expanded_query_vec, norm_doc_vects)

    return res_vect
