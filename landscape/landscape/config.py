
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
#index = 'test8'
#index = 'test10'
#index = 'test11'
index = 'test13'
# elasticsearch document type
doc_type = 'mappedTrials'

genes_index = 'landscape'
genes_doc_type = 'landscape_terms'

wordcount_index = 'wordcount'
wordcount_doc_type = 'mappedTrials'

# synonyms file name
# one default search place is $elasticsearch_home_folder/config/
# so, put the synonyms file under this folder
#synonyms_file = 'GeneSynonyms_filtered.txt'
#synonyms_file = 'GeneSynonyms_new.txt' #test10
#synonyms_file = 'GeneSynonyms_longer_than3'
synonyms_file = 'GeneSynonyms_es.txt'
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

fields = ["Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace",
                      "brief_title.whitespace","Conditions.whitespace","Exclusion Criteria.whitespace"]
fields_no_synonym = ["Purpose.normal","description.normal","Inclusion Criteria.normal","official_title.normal",
                      "brief_title.normal","Conditions.normal","Exclusion Criteria.normal"]


