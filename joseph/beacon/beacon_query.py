# Code to ingest variants sqlite db, return variants that have a True hit across the beacon network
# Author - Alex Mankovich, alex.mankovich@philips.com, Philips Research North America
# Issue - running on MacOSX will tend to return segmentation default due to a compatibility issue with _scproxy.so and OSX's SystemConfiguration framework
# 	fix is to run code as the following: env no_proxy='*' python3 beacon_query.py -vdb test_NYS.hg19.sqlite
# ~55 minutes to run

from multiprocessing import Pool, freeze_support
from functools import partial
import argparse, time
import os
from joseph.beacon.beacon_api import *
import json, sqlite3


def argParser():
	parser = argparse.ArgumentParser("""usage: %prog [options] [vcf_sqlite_DB] [beacon(s)_to_query] """)
	parser.add_argument('-vdb', type=str, help='an sqlite database created by beacon_import_data.py')
	parser.add_argument('-b', type=str, default=None, nargs='+', help='beacon(s) to query')
	args = parser.parse_args()
	return args

def getQueries(dbFile):
	# Fetch all variant entries from sqlitedb
	dbName = "test_NYS"
	conn = sqlite3.connect(dbFile)
	db = conn.cursor()
	command = """SELECT * from %s""" % dbName
	rows=db.execute(command).fetchall()
	return rows

def matchBeacons(entry, ref, b_list=None):
	# Run query_beacons from beacon_api.py with given variant entry; return true if there is a hit
	chrom, pos, allele = entry
	jsondump = query_beacons(chrom, pos, allele, ref, b_list)
	if any(result['response'] == True for result in jsondump):
		return True

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
def run():# Execute, parse, output query results
	db = "test_NYS.hg19.sqlite"
	var_queries = getQueries (os.path.join(PROJECT_ROOT, db))
	ref = db.split ('.')[1]

	beacons = list_beacons ()  # Query beacon api for list of available beacons
	beacon_ids = [beacons[x]['id'] for x in range (0, len (beacons))]
	beacon_ids.remove (
		'bob')  # Too slow to query all beacons through 'beacon of beacons'; skipping and querying beacons in parallel
	pool = Pool (15)  # 15 workers
	count = 0

	for entry in var_queries:
		count += 1
		func = partial (matchBeacons, entry, ref)
		t1 = time.strftime ("%M:%S", time.localtime (time.time ()))
		rs = "chrom:{} position:{} allele:{}".format(entry[0],entry[1],entry[2])
		yield "data:{}\n\n".format(rs)
		exist = 'False'
		for i in pool.imap_unordered (func, beacon_ids):
			if i:
				exist ='True'
				break

		yield "data:{}\n\n".format(exist)


if __name__ == "__main__":

	run()