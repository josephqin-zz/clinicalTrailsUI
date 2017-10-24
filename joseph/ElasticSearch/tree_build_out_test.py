# Code to builds searchable tree based on obo file data.
# User inputs disease term, and system outputs the disease and all parent diseases with their synonyms
# Copyright Royal Philips 2016
# Author: Alex Mankovich, alex.mankovich@philips.com, Philips Research North America
# Usage: python3 tree_build_out.py -d "lung cancer"

import re,os
import argparse
import config
from parse_obo import buildDB

#  Load Disease Ontology file
obo = open('HumanDO.obo', 'r')

#  Import into obo term class
database = buildDB(obo)

#  Extract diseases and synonyms from loaded class
diseases = [x.names for x in database]
diseases = [x.lower() for y in diseases for x in y]
synonyms = [x.synonyms for x in database]

for entry in range(0,len(synonyms)-1):
    if len(synonyms[entry]) == 1:
        synonyms[entry] = re.sub(r"(\" EXACT|\" RELATED)(.*)", "", synonyms[entry][0])
        synonyms[entry] = re.sub("\"", "", synonyms[entry])
        synonyms[entry] = re.sub(r"\([^)]*\)", "", synonyms[entry])
        synonyms[entry] = re.sub(r"\s+$", "", synonyms[entry])
    else:
        synonyms[entry] = [re.sub(r"(\" EXACT|\" RELATED)(.*)", "", x) for x in synonyms[entry]]
        synonyms[entry] = [re.sub("\"", "", x) for x in synonyms[entry]]
        synonyms[entry] = [re.sub(r"\([^)]*\)", "", x) for x in synonyms[entry]]
        synonyms[entry] = [re.sub(r"\s+$", "", x) for x in synonyms[entry]]

is_as = [x.is_as for x in database]

#  Parse parent terms out into list of lists (some entries empty, some length = 1 and > 1
for i in range(0, len(is_as)):
    if len(is_as[i]) == 1:
        split = [is_as[i][0].split(' ! ')[1].lower()]
    elif len(is_as[i]) > 1:
        split = [x.split(' ! ')[1].lower() for x in is_as[i]]
    else:
        split = is_as[i]
    is_as[i] = split

#  Construct dictionary where keys are any disease term, and values are any direct parents
obodict = dict(zip(diseases, is_as))
obosyn = dict(zip(diseases, synonyms))


def argParser():
    parser = argparse.ArgumentParser("""usage: %prog [options] [disease]""")
    parser.add_argument('-d', type=str, help='disease to find parents of')
    args = parser.parse_args()
    return args


#  Recursive function returns the parent disease at each pass until there is no parent left
#  Also prints the synonyms for each disease
def parents(query, res):
    if query == "disease":
        return False
    #return "%s - SYNONYMS: %s" % (query, obosyn[query])
    res.append({query: obosyn[query]})
    try:
        orig = obodict[query][0]
        try:
            parents(orig, res)
        except IndexError:
            pass
    except KeyError:
        print('key does not exist')
        pass


#  User enters disease of interest, does a look up in canonical
#  and synonym terms, and returns every parent disease and their synonyms.
def main(disease):
    res = []
    for i in range(0, len(synonyms)-1):
        if type(synonyms[i]) is str:
            synonyms[i] = synonyms[i].lower()
            if disease == synonyms[i]:
                disease = diseases[i]
        elif type(synonyms[i]) is list:
            synonyms[i] = [x.lower() for x in synonyms[i]]
            if disease in [x for x in synonyms[i]]:
                disease = diseases[i]
    try:
        parents(disease, res)
    except KeyError:
        print("Does not exist")
    finally:
        return res

if __name__ == "__main__":
    args = argParser()
    disease = args.d.lower()
    a = main(disease)
    for aa in a:
        print(aa)
