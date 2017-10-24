from joseph.landscape import wordcount
from joseph.models import SynLandScape
import os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def readfile(file):
	with open(os.path.join(PROJECT_ROOT,file),'r') as txt:

		lines = txt.readlines()
		for l in lines:
			term = l.split('\t')
			if term[0].__len__() > 2:
				sls = SynLandScape ()
				sls.syn = term[0]
				sls.gene = term[1].replace ('\n', '')
				try:
					obj = wordcount.LandScape(term[0].lower())
					sls.frequency = obj['total_word_count']
					sls.doc = obj['doc_count']
				except:
					sls.frequency = 0
					sls.doc = 0
				sls.save()





