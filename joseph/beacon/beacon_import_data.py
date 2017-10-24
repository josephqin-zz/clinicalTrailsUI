# Tool to convert a VCF file into a sqlite database
# utf-8 encoding, user must input 1. human genome assembly (e.g. hg19) for the file, 2. new db name, 3. source vcf file
# Contains some functions from the UCSC reference beacon implementation
# Author - Alex Mankovich, alex.mankovich@philips.com, Philips Research North America
# Modified from ucscBeacon reference implementation available at https://github.com/maximilianh/ucscBeacon
# Apache 2.0 License

import sqlite3, gzip, optparse
from os.path import join, isfile, dirname, isdir, basename, sys

from joseph.beacon.beacon_api import *


def argParser():
	# Parsing command-line arguments
	" parse command line options into args and options "
	parser = optparse.OptionParser (
		"""usage: %prog [options] [referenceDb] [datasetName] filename(s) - import VCF, complete genomics or BED files into the beacon database.""")

	(options, args) = parser.parse_args ()

	if len (args) == 0:
		parser.print_help ()
		sys.exit (0)
	return args, options


def dbCreateTable(conn, tableName):
	" create an empty table with chrom/pos/allele fields "
	conn.execute ("DROP TABLE IF EXISTS %s" % tableName)
	conn.commit ()

	_tableDef = (
		'CREATE TABLE IF NOT EXISTS %s '
		'('
		'  chrom text,'  # chromosome
		'  pos int,'  # start position, 0-based
		'  allele text'  # alternate allele, can also be IATG = insertion of ATG or D15 = deletion of 15 bp
		')')
	conn.execute (_tableDef % tableName)
	conn.commit ()


def dbFileName(refDB, datasetName):
	dbDir = dirname (__file__)
	dbName = '{0}.{1}.sqlite'.format (datasetName, refDB)
	dbPath = join (dbDir, dbName)
	return dbPath


def dbOpen(refDB, datasetName, mustExist=False):
	dbName = dbFileName (refDB, datasetName)
	if not isfile (dbName) and mustExist:
		return None
	conn = sqlite3.Connection (dbName)
	return conn


def dbGetTables(conn):
	cursor = conn.cursor ()
	cursor.execute ("SELECT name FROM sqlite_master WHERE type='table';")
	rows = cursor.fetchall ()
	tables = []
	for row in rows:
		tables.append (row[0])
	return tables


def dbQuery(conn, query, parameters):
	cursor = conn.cursor ()
	if params == None:
		cursor.execute (query)
	else:
		cursor.execute (query, parameters)
	return cursor.fetchall ()


def readAllelesVcf(ifh):
	rows = []
	skipCount = 0
	emptyCount = 0
	for chunk in ifh.chunks ():
		for line in chunk.decode ('utf-8').splitlines ():
			if line.startswith ("#"):
				continue
			fields = str.split (line.rstrip ("\n"), "\t", maxsplit=5)
			chrom, pos, varId, ref, alt = fields[:5]
			if chrom.startswith ("chr"):
				chrom = chrom.replace ("chr", "")
			pos = int (pos) - 1
			if alt == ".":
				emptyCount += 1
				continue
			refIsOne = len (ref) == 1
			altIsOne = len (alt) == 1

			if refIsOne and altIsOne:
				allele = alt
			elif not refIsOne and altIsOne:
				allele = "D" + str (len (ref) - 1)
				pos += 1
			elif refIsOne and not altIsOne:
				allele = "I" + alt[1:]
				pos += 1
			elif not refIsOne and not altIsOne:
				skipCount += 1
			else:
				print ("Invalid VCF fields:", fields)
				sys.exit (1)
			dataRow = (chrom, pos, allele)
			rows.append (dataRow)
		print ("Skipped %d lines with empty ALT alleles" % emptyCount)
		print ("Skipped %d lines with both ALT and REF alleles len!=1, cannot encode as queries" % skipCount)
	return rows


def importFiles(refDB, ifh, datasetName):
	conn = dbOpen (refDB, datasetName)
	dbCreateTable (conn, datasetName)

	conn.execute ("PRAGMA synchronous=OFF")
	conn.execute ("PRAGMA count_changes=OFF")  # http://blog.quibb.org/2010/08/fast-bulk-inserts-into-sqlite/
	conn.execute ("PRAGMA cache_size=800000")  # http://web.utk.edu/~jplyon/sqlite/SQLite_optimization_FAQ.html
	conn.execute ("PRAGMA journal_mode=OFF")  # http://www.sqlite.org/pragma.html#pragma_journal_mode
	conn.execute ("PRAGMA temp_store=memory")
	conn.commit ()


	alleles = readAllelesVcf (ifh)
	print ("Loading alleles into db %s" % dbFileName (refDB, datasetName))
	sql = "INSERT INTO %s (chrom, pos, allele) VALUES (?,?,?)" % datasetName
	conn.executemany (sql, alleles)
	conn.commit ()

	print ("Indexing db table")
	conn.execute ("CREATE UNIQUE INDEX '%s_index' ON '%s' ('chrom','pos','allele')" % \
	              (datasetName, datasetName))


def main():
	args, options = argParser ()
	refDB = args[0]
	datasetName = args[1]
	fileName = args[2]
	if len (args) < 3:
		print ("Specify refdb, datasetname, and vcf filename")
		sys.exit (1)
	if refDB not in list_references ():
		print ("The reference assembly '%s' is not valid." % refDB)
		print ("Please specify one of these reference assemblies:")
		print (list_references ())
		sys.exit (1)
	importFiles (refDB, fileName, datasetName)


if __name__ == "__main__":
	main ()
