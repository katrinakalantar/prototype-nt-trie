
# prototype-nt-trie

Tools for accessing the NCBI database using marisa trie.




### Set-up

Install marisa-trie

```bash
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
```
aws s3 cp s3://czid-public-references/ncbi-indexes-prod/2022-06-02/index-generation-2/taxid2accession.marisa .
```

For reference if creating new tries...
* Weird string notiation https://docs.python.org/3/library/struct.html#format-strings, i.e. `256pI`: a string of length 256 followed by an integer

### Usage

Can load the trie(s) and query using examples from `query-trie/play_with_trie.py`