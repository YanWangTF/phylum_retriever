#! /usr/bin/python

import os
import sys
import getopt
from Bio import Entrez

def usage():
	print 
"""
Usage: Phylum_retriever.py [-h] <List of Species or General names>

Note: If Entrez declined the accession, please kindly type in your email address in line 46.

Contact: yanxw.wang@gmail.com

-h                  print this help message

"""
Species=[]

List=sys.argv[1];

try:
	t=open(List)
except IOError:
	print("File %s does not exit!!!" % List)

filecontent=open(List)
for line in filecontent:
	Species.append(line.replace("\r\n", ""))

def Tax_ID(species):
    species = species.strip()
    handle = Entrez.esearch(term = species, db = "taxonomy", retmode = "xml")
    Output = Entrez.read(handle)
    if Output['Count'][0] is '0':
    	return "check the species name"
    else:
    	return Output['IdList'][0]

def Rank_Info(Tax_ID):
    Output = Entrez.efetch(id = Tax_ID, db = "taxonomy", retmode = "xml")
    return Entrez.read(Output)

Entrez.email = "INSERT YOUR EMAIL ADDRESS HERE"

x=open('Phylum_output.txt','a')
for a in Species:
	Taxid = Tax_ID(a)
	if type(Taxid)==str:
		x.write(a+'\t'+'Unknown Species, please check the spelling of the species name' +'\n')
	else:
		rank = Rank_Info(Taxid)
		Phylum={s['ScientificName'] for s in rank[0]['LineageEx'] if s['Rank'] in ['phylum']}
		x.write(a+'\t'+'\n'.join(Phylum) +'\n')

x.close()

