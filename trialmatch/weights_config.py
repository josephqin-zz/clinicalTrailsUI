# this file defines weights of sections in trials document.
                 # field                       section on CT website
w_purpose = '1'  # purpose                     brief_summary 
w_des = '1'      # description                 detailed_description
w_ic = '1'       # inclusion criteria          Inclusion Criteria inside Eligibility Criteria
w_ot = '1'       # official title              official_title
w_bt = '1'       # brief title                 brief_title
w_con = '1'      # condition                   all Condition sections

# if True, when query disease, it will be must(boost:3) + should(boost:0.1)
# if False, when query disease, it will be must only. 
# i.e., if False, only all terms of queried disease occur will be treated as a match
use_should = False

# https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html
# default is 'best_fields'
multi_match_type = 'cross_fields' #'cross_fields'
# defalut is 'or' 
multi_match_operator = 'and'  # 'and'

# boost value of must for field 'disease', 'gene', and 'aas':
boost_must_value = 3
# boost value of shoud for field 'disease', 'gene', and 'aas':
boost_should_value = 0.1
