# Code to import each obo term into a python class object
# Copyright Royal Philips 2016
# Author: Alex Mankovich, alex.mankovich@philips.com, Philips Research North America

import re

class oboTerm:
	#class for maintaining obo data structure for each term 
	def __init__(self):
		self.ids = []
		self.names = []
		self.namespaces = []
		self.alt_ids = []
		self.defs = []
		self.comments = []
		self.subsets = []
		self.synonyms = []
		self.xrefs = []
		self.is_as = []
		self.created_bys = []
		self.creation_dates = []

	def add_id(self, identifier):
		self.ids.append(identifier)

	def add_name(self, name):
		self.names.append(name)

	def add_namespace(self, namespace):
		self.namespaces.append(namespace)

	def add_alt_id(self, alt_id):
		self.alt_ids.append(alt_id)

	def add_def(self, definition):
		self.defs.append(definition)

	def add_comment(self, comment):
		self.comments.append(comment)

	def add_subset(self, subset):
		self.subsets.append(subset)

	def add_synonym(self, synonym):
		self.synonyms.append(synonym)

	def add_xref(self, xref):
		self.xrefs.append(xref)

	def add_is_a(self, is_a):
		self.is_as.append(is_a)

	def add_created_by(self, created_by):
		self.created_bys.append(created_by)

	def add_creation_date(self, creation_date):
		self.creation_dates.append(creation_date)

def buildDB(file):
	count=-1
	terms = []
	for line in file:
		#find term attributes, restructure, store
		if re.match("id:(.*)",line):
			count += 1
			terms.append(None)
			# print(terms[count])
			terms[count] = oboTerm()
			terms[count].add_id(re.sub("id: ","",re.sub(r"\n","",line)))
		elif re.match("name:(.*)",line):
			terms[count].add_name(re.sub("name: ","",re.sub(r"\n","",line)))
		elif re.match("namespace:(.*)",line):
			terms[count].add_namespace(re.sub("namespace: ","",re.sub(r"\n","",line)))
		elif re.match("alt_id:(.*)",line):
			terms[count].add_alt_id(re.sub("alt_id: ","",re.sub(r"\n","",line)))
		elif re.match("def:(.*)",line):
			terms[count].add_def(re.sub("def: ","",re.sub(r"\n","",line)))
		elif re.match("comment:(.*)",line):
			terms[count].add_comment(re.sub("comment: ","",re.sub(r"\n","",line)))
		elif re.match("subset:(.*)",line):
			terms[count].add_subset(re.sub("subset: ","",re.sub(r"\n","",line)))
		elif re.match("synonym:(.*)",line):
			terms[count].add_synonym(re.sub("synonym: ","",re.sub(r"\n","",line)))
		elif re.match("xref:(.*)",line):
			terms[count].add_xref(re.sub("xref: ","",re.sub(r"\n","",line)))
		elif re.match("is_a:(.*)",line):
			terms[count].add_is_a(re.sub("is_a: ","",re.sub(r"\n","",line)))
		elif re.match("created_by:(.*)",line):
			terms[count].add_created_by(re.sub("created_by: ","",re.sub(r"\n","",line)))
		elif re.match("creation_date:(.*)",line):
			terms[count].add_creation_date(re.sub("creation_date: ","",re.sub(r"\n","",line)))
		elif re.search("\[Typedef\]",line): #entry contains metadata at EOF and not useful, skip
			break
		elif re.search("\[Term\]",line):
			continue #entry not useful, skip
		elif line in ['\n', '\r\n']:
			continue #entry empty, skip
		else:
			continue #entry not recognized, skip
	return terms
