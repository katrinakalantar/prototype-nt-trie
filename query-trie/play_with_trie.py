'''
play_with_trie.py

Created by Katrina Kalantar, Oct 4 2022

This script loads the taxid2accession.marisa trie and gets sequences associated with all accessions of that taxid.
Intended as a playground to show example usage of the trie for querying.

'''

import marisa_trie
import boto3

from botocore import UNSIGNED
from botocore.client import Config

taxid2accession_trie = marisa_trie.RecordTrie("30p").mmap("taxid2accession.marisa")

def get_sequence(this_trie, accession, db):
    (seq_offset, header_len, seq_len), = this_trie[accession]
    to = seq_offset + header_len + seq_len - 1
    if db == 'NT':
        return(boto3.resource('s3', config=Config(signature_version=UNSIGNED)).Object("czid-public-references", "ncbi-indexes-prod/2022-06-02/index-generation-2/nt").get(Range=f'bytes={seq_offset}-{to}')['Body'].read())
    elif db == 'NR':
        return(boto3.resource('s3', config=Config(signature_version=UNSIGNED)).Object("czid-public-references", "ncbi-indexes-prod/2022-06-02/index-generation-2/nr").get(Range=f'bytes={seq_offset}-{to}')['Body'].read())

nr_loc_trie = marisa_trie.RecordTrie("QII").mmap('marisa_refs/nr_loc.marisa')
nt_loc_trie = marisa_trie.RecordTrie("QII").mmap('marisa_refs/nt_loc.marisa')

MY_TAXID = '40324'

all_accessions_for_this_taxid = taxid2accession_trie[MY_TAXID]
for acc in all_accessions_for_this_taxid:
    actual_keys_nr = nr_loc_trie.keys(acc[0].decode("utf-8"))
    actual_keys_nt = nt_loc_trie.keys(acc[0].decode("utf-8"))
    print("actual keys (nr)")
    print(actual_keys_nr)
    print("actual keys (nt)")
    print(actual_keys_nt)
    for ak in actual_keys_nr:
        seq = get_sequence(nr_loc_trie, ak, "NR")
        print(seq)
    for ak in actual_keys_nt:
        seq = get_sequence(nt_loc_trie, ak, "NT")
        print(seq)
