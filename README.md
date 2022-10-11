

# prototype-nt-trie

Tools for accessing the NCBI database using marisa trie.

The NCBI database is huge and difficult to query using existing tools. The CZ ID team developed some key/value stores to contain various parts of the NCBI databases and enable much more efficient querying. These files rely on the marisa-trie data structure. More information can be found here: https://github.com/pytries/marisa-trie. 

Specifically,
* `accession2taxid.marisa` contains key = accession, value = taxid -- allows rapid look-up of taxid for an associated accession
```
WP_189720600  # accession 
[(40324,)]    # taxid (in a tuple)
WP_189720601
[(40324,)]
```

* `taxid2accession.marisa` contains key = taxid, value = accession -- allows rapid look-up of all accessions for a particular taxid
```
2026735    # taxid
# accessions (as list of tuples)
[(b'MBW2272000',), (b'MBW2272001',), (b'MBW2272002',), (b'MBW2272003',), (b'MBW2272004',), (b'MBW2272005',), (b'MBW2272006',), (b'MBW2272007',), (b'MBW2272008',), (b'MBW2272009',)]
```
* `nr_loc.marisa` contains key = accession, value = location -- allows rapid look-up of sequence locations (in the NCBI NR DB) by accession; the location values can then be used to access raw sequences associated with each accession.
```
WP_189720600.1.            # accession
[(58532278831, 203, 493)]  # location, triplet of values (seq_offset, header_len, seq_len)
WP_189720601.1
[(6838193903, 143, 221)]
```
* `nt_loc.marisa` contains key = accession, value = location -- allows rapid look-up of sequence locations (in the NCBI NT DB) by accession; the location values can then be used to access raw sequences associated with each accession.
```
same as above, but for NT database
XM_039400000.1
[(136943594771, 101, 2417)]
XM_039400001.1
[(136912702546, 122, 2328)]
```
* `nt_info.marisa` contains key = accession, value = info about accession (DEFINITION and LENGTH) fields from accession entries -- allows rapid lookup of supporting details about accession sequence
```
XM_039400000.1    # accession
# "INFO" about the accession
[(b'PREDICTED: Styela clava solute carrier family 22 member 12-like (LOC120332697), mRNA\n', 2387)]
XM_039400001.1
[(b'PREDICTED: Styela clava hercynylcysteine sulfoxide lyase-like (LOC120332696), transcript variant X1, mRNA\n', 2299)]
```
* `taxid-lineages.marisa` contains key = taxid, value = triplet of taxids for species / genus / family- level classification -- allows rapid lookup of species / genus / family taxon lineage
```
1829300                    # taxid
[(1829300, -200, 92557)]   # lineage, triplet of ("SPECIES", "GENUS", "FAMILY")
182930
[(182930, 182922, 400783)]
```

For initial experiments related to NCBI DB redundancy, the `taxid2accession.marisa` and `[nt|nr]_loc.marisa` files may be most relevant.


### Set-up

Install marisa-trie

```bash

# if using virtualenv
python3 -m venv marisa-trie-env
source ./marisa-trie-env/bin/activate

# install necessary python libraries
pip install marisa-trie
pip install boto3

```

Download the k/v stores

These are the k/v stores that exist as part of CZ ID index generation process
```bash
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/accession2taxid.marisa .
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/nr_loc.marisa .
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/nt_loc.marisa .
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/nt_info.marisa .
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/taxid-lineages.marisa .
```

This is the k/v store created by ./create-trie/trie_update.py
```bash
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/taxid2accession.marisa .
```

For reference, the .marisa files range in size but are generally ~2GB
```bash
2.1G accession2taxid.marisa
2.1G taxid2accession.marisa
3.1G nt_info.marisa
5.4G nr_loc.marisa
925M nt_loc.marisa
16M taxid-lineages.marisa
```



For reference if creating new tries...
* Weird string notation https://docs.python.org/3/library/struct.html#format-strings, i.e. `256pI`: a string of length 256 followed by an integer

### Usage

Can load the trie(s) and query using examples from `query-trie/preview_tries.py` or `query-trie/play_with_trie.py` 




### Downstream application

**One Idea - Sourmash Taxonomic Relatedness**

Can gather all sequences for a particular taxid (i.e. into `output.fasta` via script `get_seqs_by_taxid.py`), and then use something like sourmash to evaluate relatedness.

```bash
sourmash compute --singleton -k=21 --scaled=10000 output.fasta
sourmash compare output.fasta.sig -o cmp
sourmash plot cmp
```