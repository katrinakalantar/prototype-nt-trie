
# prototype-nt-trie

Tools for accessing the NCBI database using marisa trie.




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

Can load the trie(s) and query using examples from `query-trie/play_with_trie.py`
