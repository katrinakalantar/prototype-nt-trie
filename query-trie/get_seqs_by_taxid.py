'''
get_seqs_by_taxid.py

Written by Katrina Kalantar, Oct 5 2022

Usage:
python3 get_seqs_by_taxid.py NT 2697049

Output a .fasta file containing all sequences from [NT | NR] NCBI database 
that belong to taxid = 2697049 (sars-cov-2).

'''


import marisa_trie
import boto3

from botocore import UNSIGNED
from botocore.client import Config

import sys


database = sys.argv[1]
taxid = sys.argv[2]

print(database)
print(taxid)

taxid2accession_trie = marisa_trie.RecordTrie("30p").mmap("marisa_refs/taxid2accession.marisa")

def get_sequence(this_trie, accession, db):
    (seq_offset, header_len, seq_len), = this_trie[accession]
    to = seq_offset + header_len + seq_len - 1
    if db == 'NT':
        return(boto3.resource('s3', config=Config(signature_version=UNSIGNED)).Object("czid-public-references",
            "ncbi-indexes-prod/2022-06-02/index-generation-2/nt").get(Range=f'bytes={seq_offset}-{to}')['Body'].read())
    elif db == 'NR':
        return(boto3.resource('s3', config=Config(signature_version=UNSIGNED)).Object("czid-public-references",
            "ncbi-indexes-prod/2022-06-02/index-generation-2/nr").get(Range=f'bytes={seq_offset}-{to}')['Body'].read())

def process_seq(seq):
    seq_str = seq.decode("utf-8")
    print(seq_str)
    print(seq_str.split('\n'))

if database == "NT":
    print("database == NT")
    trie_file = 'marisa_refs/nt_loc.marisa'
elif database == "NR":
    print("database == NR")
    trie_file = 'marisa_refs/nr_loc.marisa'

relevant_trie = marisa_trie.RecordTrie("QII").mmap(trie_file)

all_accessions_for_this_taxid = taxid2accession_trie[taxid]
all_sequences = []

for acc in all_accessions_for_this_taxid:
    actual_keys = relevant_trie.keys(acc[0].decode("utf-8"))
    for ak in actual_keys:
        seq = get_sequence(relevant_trie, ak, database)
        #print(seq)
        all_sequences.append(seq.decode("utf-8"))

fasta_output = ''.join(all_sequences)
output_file = open("output.fasta", "w")
output_file.write(fasta_output)
output_file.close()


print("completed script")