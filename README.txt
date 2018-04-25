This is the README file for A0179092W-A0175111U-A0179365N-A0179262X's submission

== Python Version ==

We're using Python Version 2.7.12 for this assignment.

== General Notes about this assignment ==

INDEX PHASE:

-> We build a positional dictionary and its postings.
-> In addition, we also create a metadata dictionary and a thesaurus, which are both used in the search phase.
-> In the positional dictionary, we store the term and it’s document frequency and also the head and tail byte for the location of its postings list in the postings file.
-> The dictionary also stores the document normalization values to be used for cosine normalization of each document. We also store the total number of documents N in the dictionary.
-> In the postings list, for each term we store it’s postings list in the form for example “docId1-pos11-pos12 docId2-pos21-pos22-pos23 docId3-pos31-pos32” 
-> The metadata dictionary stores the title of case, name of court and date posted for each document.



SEARCH PHASE:

A) Boolean retrieval:
-> For phrases, we use positional dictionary to retrieve only documents that contain the exact phrase. This is done by intersecting the positions of each term in the phrase and taking into account the relative adjacent positions in the documents.
-> For a singular freetext term, we just fetch it’s entire postings.
-> We perform the AND operation between phrases and/or singular freetext terms using the AND merging algorithm for postings
-> As an additional step, we then convert the entire query into freetext and append the output obtained from that to the result as well. For example  “Good Morning” AND “New York” is converted to the fully freetext form ‘Good Morning New York’ to compute it’s output.

B) Freetext retrieval:
-> We ranked documents by cosine similarity based on tf×idf. We implemented the lnc.ltc ranking scheme (i.e., log tf and idf with cosine normalization for queries documents, and log tf, cosine normalization but no idf for documents) 


ZONES AND FIELDS
-> We use the zone and field data like court name and date posted of the document to tweak the cosine similarity scores for the documents.
-> We defined a dictionary where we assign a relevance factor to each court name, with higher values (say 1.5) courts like “UK Supreme Court” and “SG Court of Appeal", intermediate values like 0.75 to courts like “SG High Court” and "UK High Court" and finally low values like 0.25 to courts like "SG Privy Council" and "NSW Local Court". This is based on the idea the rulings on a matter by supreme court are more relevant than high court, which are more relevant that other lower courts.
-> Similarly we assign a relevance factor to based on date posted of the document, which is to say that if document is from last 5 years we assign it value 1.5, if from last 5-10 years then value 1.0 and so on if more than 40 years old, then relevance factor of 0.2. This is based on the idea that more recent rulings/verdicts are more relevant.
-> We assigned a weightage to each of the date posted based relevance factor(0.4) and to the court name based relevance factor(0.6). This was because we thought the court which offers the ruling is more important that the date of the document.
-> The metadata zones based ranking can be turned on by setting the variable zones_metadata_switch to True in search.py file


QUERY EXPANSION TECHNIQUES

We have a provided a detailed analysis of using these query expansion techniques on results in bonus.txt

1) Synonyms : WordNet-Query expansions:
-> In case any term in the query isn’t in the dictionary, we find a single synonym for it from the WordNet synonyms list which is in our dictionary and use that to replace that term in the query.


2) Synonyms : Thesaurus
-> The index phase also generates a thesaurus from the words in the corpus, and gives us a list of all terms in corpus, which are similar to a given term. This can be used to either expand the query with additional related terms, which increases recall, or substitute terms. This helps us change the query vector for retrieving more relevant documents. 


3) Pseudo Relevance Feedback : Rocchio formula
-> For freetext retrieval, we do a round of pseudo relevance feedback assuming the top 1% of the initially retrieved documents are relevant. We then use Rocchio's formula to generate the expanded query, and then perform another round of cosine similarity computation with this new expanded query to generate the final list of ranked retrieval documents.

-> We used the following values of the constants in the rocchio formula 
alpha = 1
beta = 0.75
gamma = 0.15



OPTIMIZATIONS:
-> Stemming optimization
We observed that indexing was taking too long (about 1 hour or so). We discovered that stemming was the bottleneck for slowing down the indexing phase. Because we don’t have control over the library operations for stemming, we decided to do local caching of stem words for speed up. For each new word that we get, we store the original word as key and its stemmed value as value in a locally cached dictionary. So next time, before we attempt to stem a word, we first check if the word already has its stem present in the cache before calling the library stem function. This halved the indexing time for us, and we were able to index in about 25~28 minutes now.
 

OTHER EXPERIMENTS:
(not part of current code)

-> We tried to create a bigram and trigram dictionary that turned out to be too large and went beyond 4GB of memory, which is the reason we are currently using positional indexing.

-> We tried with converting boolean queries to complete freetext queries and get their output. Even though this was giving a higher recall which means some of the relevant documents didn’t contain the exact phrase as they weren’t being retrieved by the positional index based system , it also gave a lower precision since more documents were being retrieved now and the relevant documents were lower up in the ranking order. So while this was useful, we couldn’t just use this. So we first output the result of phrase search using positional and then the output of fully freetext query.

-> We examined some documents and found that there were 16 documents in the datatset.csv which had duplicate document Id's. They are -
247336
2044863
2145566
2147493
2148198
2167027
2225321
2225341
2225516
2225597
2225598
3062427
3062433
3063259
3063522
3926753
The two copies of the documents with these document id's had the same content but different court names in most cases. This duplication of data while not a major roadblock, was affecting our term freqeuncy and document normlization calculations by a small value.


ORIGINAL IDEAS
-> In dealing with boolean queries, we used the unique idea of first printing the output of the boolean query as we did in HW2 and then converting the entire query to fully freetext and then outputting it's output. This helped to significantly improve our score on the leaderboard.

-> We used several query expansion ideas like metadata, rocchio, thesaurus and wordnet for synonyms.

-> We used the stemming optimization to remedy the bottleneck and speed up indexing.



DISTRIBUTION OF WORK
A0179092W ->
A0175111U -> 
A0179365N ->
A0179262X -> building dictionary and postings, metadata zones and fields implementation, free text retrieval in search

== Files included with this submission ==

index.py
Generate the dictionary and the postings files from the Intellex training data set.

search.py
Load the dictionary, read and evaluate all queries and write their results to the output file.

boolean_retrieval.py
Handle boolean queries that are composed of either single terms or phrases of max. length 3 (a phrase in written in quotes)

freetext_retrieval.py
Handle free text queries that using tf-idf as in assignment 3.

retrieve_postings.py
This module contains the methods for handling synonyms and retrieving the postings for a given term or its synonyms.

synonyms.py
This module uses wordnet to return synonyms and their postings for a given term.

thesaurus.py
This module builds a co-occurrence matrix out from the term document matrix, which is built during index itself, based
on the terms from the corpus, and for any given term, it gives us the list of the most similar terms in the corpus
(using the term document similarity weights).

dictionary.txt
The dictionary with terms and their head, tail and document frequency.

postings.txt
The positional postings for all terms in the dictionary. It includes their positions in the respective document.

README.txt
The description of our approach and other important notes.

== Statement of individual work ==

[x] We, A0179092W-A0175111U-A0179365N-A0179262X, certify that we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

Emails: e0268461@u.nus.edu
    e0268631@u.nus.edu
    e0268734@u.nus.edu
    e0215813@u.nus.edu
    

== References ==
Websites as reference:
https://stackoverflow.com/ - used for some python related questions.
https://docs.python.org/2.7/ - (official Python documentation) - used for other python related questions



