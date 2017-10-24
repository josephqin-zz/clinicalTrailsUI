
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
#index = 'test13'  #2016 source of synonym, latest trials (7/20) downloaded.
index = 'test14'  # new disease synonym file. all canonical forms are single word.
# elasticsearch document type
doc_type = 'mappedTrials'

#wordcount_index = 'wordcount'
wordcount_index = 'wordcount2'  # with case sensitive
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
synonyms_file_case_sensitive = 'GeneSynonyms_1018_es.txt'

# disease synonyms file name
disease_synonym_file = 'new_disease_synonym.txt'

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

# no : No term vectors are stored. (default)
# yes : Just the terms in the field are stored.
# with_positions : Terms and positions are stored.
# with_offsets : Terms and character offsets are stored.
# with_positions_offsets : Terms, positions, and character offsets are stored.
term_vector = 'with_positions'

fields = ["Purpose","description","Inclusion Criteria","official_title",
        "brief_title","Conditions","Exclusion Criteria"]

#fields_punctuation = ["Purpose.whitespace","description.whitespace","Inclusion Criteria.whitespace","official_title.whitespace",
#                      "brief_title.whitespace","Conditions.whitespace","Exclusion Criteria.whitespace"]
fields_no_synonym = ["Purpose.normal","description.normal","Inclusion Criteria.normal","official_title.normal",
                      "brief_title.normal","Conditions.normal","Exclusion Criteria.normal"]
fields_no_syn_case_sstv = ["Purpose.standard_case","description.standard_case","Inclusion Criteria.standard_case",
                           "official_title.standard_case","brief_title.standard_case","Conditions.standard_case",
                           "Exclusion Criteria.standard_case"]
#fields_no_synonym = ["Conditions.normal"]
