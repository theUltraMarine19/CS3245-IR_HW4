import json

def fetch_thesaurus(term):
	with open('thesaurus.txt') as thesau_f:
		thesaurus =  json.load(thesau_f)

		return thesaurus[term]
