'''
gather_description_data_by_species.py

Written by Katrina Kalantar, Oct 11 2022

Usage:
python3 gather_description_data_by_species.py [taxid]
Output a .tsv file containing [accision ID] / [description] / [seq_length] for all accessions
...associated with a particular taxID of interest
'''

import marisa_trie
import sys

# by accession, get description
nt_info_trie = marisa_trie.RecordTrie("256pI").mmap('marisa_refs/nt_info.marisa')
# by taxid, get all accessions related to it
taxid_to_accession_trie = marisa_trie.RecordTrie("30p").mmap("marisa_refs/taxid2accession.marisa")

count = 0

taxid_of_interest = sys.argv[1] 
print(taxid_of_interest)

data_strings_list = []
output_file = open('output_descriptions_' + str(taxid_of_interest) + '.tsv','w')

accessions_for_this_taxid = taxid_to_accession_trie[taxid_of_interest]
for acc in accessions_for_this_taxid:
    actual_keys = nt_info_trie.keys(acc[0].decode("utf-8"))
    for ak in actual_keys:
        #print(ak)
        description = nt_info_trie[ak][0][0]
        length = nt_info_trie[ak][0][1]
        #print(description)
        #print(length)
        this_data_string = ak + '\t' + description.decode("utf-8").strip() + '\t' + str(length) + '\n'
        output_file.write(this_data_string)

output_file.close()