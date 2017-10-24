import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# project home folder, make sure ends with /
home = '/home/ec2-user/TrialMatching_transfer/'

# folder to store downloaded xml trial files
# make sure ends with /
#xml_folder = home + 'latest/'  # $home/latest/
xml_folder = '/home/ec2-user/TrialMatching_backup/trials_7_20/'

# the file that contains all valid stages
all_stages_path = home + 'stageInformation.txt'

# elasticsearch index
#index = 'testing'
#index = 'test7'   # disease synonym
#index = 'test8'
#index = 'test9'
#index = 'test10'
#index = 'test11'
#index = 'test12'
# fixed bug in extractInfo.py
index = 'test14'  #2016 source of synonym, latest trials (7/20) downloaded.
# elasticsearch document type
doc_type = 'mappedTrials'

wordcount_index = 'wordcount'
wordcount_doc_type = 'mappedTrials'

# gene synonyms file name
# one default search place is $elasticsearch_home_folder/config/
# so, put the synonyms file under this folder
#synonyms_file = 'GeneSynonyms.txt'
#synonyms_file = 'GeneSynonyms_filtered.txt'   #test8
#synonyms_file = 'GeneSynonyms_empty.txt'  #test9
#synonyms_file = 'GeneSynonyms_new.txt'  #test 10
#synonyms_file = 'GeneSynonyms_longer_than3.txt'  #test 11
synonyms_file = 'GeneSynonyms_es.txt'

# disease synonyms file name
disease_synonym_file = 'synonym_disease.txt'

# slop of disease terms when querying
slop = 3

# set it to True if proxy is required to
# access clinicaltrials.gov using current network
use_proxy = False

# proxy server
# if use_proxy is no, then just ignore this variable
proxy = ""


# format of output
# 1: only output results from this tool
# 2: output results from both this tool and ct.gov, and give the difference
output_format = 1
# if set to true, the program will write matched document content with ID
# to a file in json format.
# otherwise, it will only print matched document ID.
output_details = False




