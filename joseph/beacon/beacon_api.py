# Code to execute Beacon Network queries
# API documentation here: https://beacon-network.org/#/developers/api/beacon-network#bn-beacons
# Queries supported:
	# List of beacons
	# Show a beacon
	# List of organizations
	# Show an organization
	# Query beacons
	# Query a beacon
	# List supported chromosomes
	# List supported alleles
	# List supported reference genomes
# Author - Alex Mankovich, alex.mankovich@philips.com, Philips Research North America

import requests
from requests.auth import HTTPDigestAuth
import json, sqlite3


def _url(path):
	return 'https://beacon-network.org' + path

def list_beacons():
	return requests.get(_url('/api/beacons/')).json()

def show_beacon(beacon_id):
	return requests.get(_url('/api/beacons/{:d}/'.format(beacon_id))).json()

def list_organizations():
	return requests.get(_url('/api/organizations/')).json()

def show_organization(organization_id):
	return requests.get(_url('/api/organizations/{:d}/'.format(organization_id))).json()

def query_beacons(chrom, pos, allele, ref, beacon_ids=None):
	if beacon_ids:
		return requests.get(_url('/api/responses?chrom={0}&pos={1}&allele={2}&ref={3}&beacon={4}'.format(chrom, pos, allele, ref, beacon_ids))).json()
	else:
		return requests.get(_url('/api/responses?chrom={0}&pos={1}&allele={2}&ref={3}'.format(chrom, pos, allele, ref, beacon_ids))).json()

def list_chromosomes():
	return requests.get(_url('/api/chromosomes/')).json()

def list_alleles():
	return requests.get(_url('/api/alleles/')).json()

def list_references():
	return requests.get(_url('/api/references/')).json()

