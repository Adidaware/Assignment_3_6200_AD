""" This program is designed to test the functions the nt_fasta_stats.py """
import tempfile
import pytest
from nt_fasta_stats import (get_fasta_lists, _verify_lists, _get_num_nucleotides,
                            _get_ncbi_accession, print_sequence_stats)

def test_get_fasta_lists():
    """ Test that get_fasta_lists correctly parses FASTA data """
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_fasta:
        temp_fasta.write(">header1\nATGC\n>header2\nATGC")
        temp_fasta.close()

        headers, sequences = get_fasta_lists(temp_fasta.name)
        assert headers == ['>header1', '>header2']
        assert sequences == ['ATGC', 'ATGC']

def test_verify_lists():
    """ Test that _verify_lists correctly verifies header and sequence lists """
    headers = ['>header1', '>header2']
    sequences = ['ATGC', 'ATGC']
    _verify_lists(headers, sequences)  # Should not raise an error

    headers = ['>header1', '>header2']
    sequences = ['ATGC']
    with pytest.raises(SystemExit):
        _verify_lists(headers, sequences)

def test_get_num_nucleotides():
    """ Test that _get_num_nucleotides correctly outputs the nucleotide sequence """
    sequence = "ATGCN"
    assert _get_num_nucleotides('A', sequence) == 1
    assert _get_num_nucleotides('G', sequence) == 1
    assert _get_num_nucleotides('C', sequence) == 1
    assert _get_num_nucleotides('T', sequence) == 1
    assert _get_num_nucleotides('N', sequence) == 1

def test_get_ncbi_accession():
    """ Test that _get_ncbi_accession correctly returns the accession number """
    header = ">NCBI_accession"
    assert _get_ncbi_accession(header) == ">NCBI_accession"

def test_print_sequence_stats():
    """ Test that the _print_sequence_stats function correctly prints
    the header and sequence stats """
    headers = ['>header1', '>header2']
    sequences = ['ATGC', 'ATGC']
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_out:
        print_sequence_stats(headers, sequences, temp_out.name)
