'''
preview_tries.py 

Written by Katrina Kalantar, Oct 5 2022

This script opens each .marisa file (downloaded from s3 and put into a directorion ./marisa_refs) and loads
the data. It prints out the top N keys / values from within the trie.

'''

import marisa_trie

def preview_trie(this_trie, max_keys=10):
    count = 0
    for k in this_trie:
        count +=1
        print(k)
        len_of_output = len(this_trie[k])
        print(this_trie[k][0:min(10, len_of_output)])
        if count > max_keys:
            break

# For each available marisa trie structure, this code demonstrates...
# 1. how to load the trie into use within a python script (varies by data type)
# 2. applies the `preview_trie` function to print out the top N (default = 10) key/value pairs

# taxid-lineages.marisa trie -- key = taxid, value = lineage triplet of ("SPECIES", "GENUS", "FAMILY")
taxid_lineage_trie = marisa_trie.RecordTrie("lll").mmap('marisa_refs/taxid-lineages.marisa')
print("\n--- previewing taxid_lineages trie ---\n")
preview_trie(taxid_lineage_trie)

# nt_info.marisa trie -- key = accession, value = triplet of ("DEFINITION", "LENGTH")
nt_info_trie = marisa_trie.RecordTrie("256pI").mmap('marisa_refs/nt_info.marisa')
print("\n--- previewing nt_info trie ---\n")
preview_trie(nt_info_trie)

# accession2taxid.marisa trie -- key = accession, value = taxid
accession_to_taxid_trie = marisa_trie.RecordTrie("Q").mmap('marisa_refs/accession2taxid.marisa')
print("\n--- previewing accession_to_taxid trie ---\n")
preview_trie(accession_to_taxid_trie)

# taxid2accession.marisa trie -- key = taxid, value = list of tuples with format (accession, [empty] )
taxid_to_accession_trie = marisa_trie.RecordTrie("30p").mmap("marisa_refs/taxid2accession.marisa")
print("\n--- previewing taxid_to_accession trie ---\n")
preview_trie(taxid_to_accession_trie, max_keys = 3) # this one is a bit slow to output due to large value lists

# nr_loc.marisa trie -- key = accession, value = triplet of (seq_offset, header_len, seq_len) ...
#    ... where `seq_len` is actually slightly inaccurate because it includes "\n" characters within the seq
#    ... based on 81bp fasta file line limit. To get accurate length, apply formula ( seq_len - (seq_len/81) )
nr_loc_trie = marisa_trie.RecordTrie("QII").mmap('marisa_refs/nr_loc.marisa')
print("\n--- previewing nr_loc trie ---\n")
preview_trie(nr_loc_trie)

# nt_loc.marisa trie -- key =  accession, value = triplet of (seq_offset, header_len, seq_len) ...
#    ... with same considerations as above
nt_loc_trie = marisa_trie.RecordTrie("QII").mmap('marisa_refs/nt_loc.marisa')
print("\n--- previewing nt_loc trie ---\n")
preview_trie(nt_loc_trie)