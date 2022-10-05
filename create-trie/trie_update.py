'''
trie_update.py

Created by Katrina Kalantar, Oct 4 2022
Load in accession2taxid.marisa trie, loop through and create taxid2accession_trie.marisa
This script only needs to be run once to create the output. This will then be query-able. 

'''

import marisa_trie
import boto3

from botocore import UNSIGNED
from botocore.client import Config

accession2taxid_trie = marisa_trie.RecordTrie("Q").mmap('marisa_refs/accession2taxid.marisa')


# example of looping through top N entries in a trie
counter = 0
max_loop_entries = 5


def my_generator_tst():
    for k in accession2taxid_trie:
        accession = k
        taxid = accession2taxid_trie[k][0][0]
        #print(accession)
        #print(taxid)
        yield(str(taxid), (str(k).encode(),))
marisa_trie.RecordTrie("30p", my_generator_tst()).save("taxid2accession.marisa")
