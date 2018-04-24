This is the README file for A0179092W-A0175111U-A0179365N-A0179262X's submission

== Python Version ==

We're using Python Version 2.7.12 for this assignment.

== General Notes about this assignment ==

Indexing phase:


Search phase:

Query expansions:
- WordNet

Optimizations:



Experiments that are not included in the current code: 
- we tried to create a bigram and trigram dictionary that turned out to be too large and went beyond 4GB of memory, which is the reason we are currently using positional indexing.


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
This module uses wordnet to return synonyms and the postings of the synonyms for a given term.

thesaurus.py
This module builds a co-occurrence matrix out from the term document matrix, 

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
