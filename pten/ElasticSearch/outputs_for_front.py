import os
import re
import json
from collections import OrderedDict
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import xml.etree.ElementTree as etree
from pten.ElasticSearch import config


def tool_only(response):
    count = 0
    st = "Total number of results : "+str(response['hits']['total'])
    print(st)
    res = []
    for hit in response['hits']['hits']:
        count = count + 1
        cur_dict = {}
        cur_dict['id'] = str(hit['_id'])
        cur_dict['score'] = hit['_score']
        cur_dict['context'] = hit['_source']

        res.append(cur_dict)
        #st = str(count) + ": " + str(hit['_id']) + ", score: " + str(hit['_score']) 
        #st = str(count) + ": " + str(hit['_id']) + ", score: " + str(hit['_score']) + ', ' + str(hit['_source']['update_date'])
        #print(st)
    #print(len(ids))
    #print(ids)
    return res,response['hits']['total']

def tool_and_ctgov(response, args, gender, age):
    dummyPath = config.home + "dummyfile.xml"
    f = open(dummyPath,'wb+')
    arr = []
    for hit in response['hits']['hits']:
        arr.append(hit['_id'])
    
    print("Trial outputs from the CT website:")
    
    term = ""
    if args.disease is not None:
        for word in args.disease.split(" "):
            term = term + word + "+"
    if args.gene is not None:
        term = term + args.gene + "+"
    if args.aas is not None:
        term = term + args.aas + "+"
    if args.stage is not None:
        for word in args.stage.split(" "):
            term = term + word + "+"
    
    with open("lastUpdated.txt",'r') as fu:
        lastUpdated = fu.read()
    url = "https://clinicaltrials.gov/ct2/results?term=" + term + "&recr=Open&rslt=Without&type=Intr" + gender + age +"&pg={}&displayxml=true&rcv_e="
    match = re.search("last updated on :.*",lastUpdated)
    if match is not None:
        [month,day,year] = match.group(0)[17:].split('/')
        url = url + month + "%2F" + day + "%2F" + "20" + year
    num = 1
    finalURL = url.format(num)
    print(finalURL)
    
    arrCT = []
    
    try:
        data = urllib2.urlopen(finalURL).read()
        f.write(data)
        f.close()
    except urllib2.HTTPError as e:
        print( e.code)
        sys.exit()
    except urllib2.URLError as e:
        print (e.args)
        sys.exit()

    searchPage = etree.parse(dummyPath)
    searchroot = searchPage.getroot()
    count = 0

    while searchroot.findall('clinical_study'):
        for study in searchroot.findall('clinical_study'):
            nctId = study.find('nct_id').text
            count = count + 1
            st = str(count) + ":" + str(nctId)
            arrCT.append(nctId)
            if nctId not in arr:
                print(st + " - Not there in tool results")
            else:
                print(st)
        num = num +1
        finalURL = url.format(num)
        f = open(dummyPath,'wb+')

        try:
            #print(str(num) + " page")
            data = urllib2.urlopen(finalURL).read()
            f.write(data)
            f.close()
        except urllib2.HTTPError as e:
            print( e.code)
            sys.exit()
        except urllib2.URLError as e:
            print (e.args)
            sys.exit()

        searchPage = etree.parse(dummyPath)
        searchroot = searchPage.getroot()

    count = 0
    st = "Total number of results : "+str(response['hits']['total'])
    print(st )
    for hit in response['hits']['hits']:
        count = count + 1
        st = str(count) + ": " + str(hit['_id'])
        if hit['_id'] not in arrCT:
            print(st + " -- Not there in CT results")
        else:
            print(st)

    os.remove(dummyPath)

def output_details_in_json(response, search_factors):
    count2 = 0
    with open('matched_doc_content.txt', 'w') as fw1:
        fw1.write('Search Criteria:\n')
        fw1.write(','.join(search_factors))
        st = "\nTotal number of results : "+str(response['hits']['total'])+'\n'
        fw1.write(st)
        sort_order = ['_index', '_type', '_id', '_score', '_source']
        hits = response['hits']['hits']
        hits_ordered = [OrderedDict(sorted(item.items(), key=lambda k: sort_order.index(k[0])))
                        for item in hits]
        content = json.dumps(hits_ordered,indent=4,separators=(',', ': '))
        fw1.write(content)
        fw1.write('\n')

