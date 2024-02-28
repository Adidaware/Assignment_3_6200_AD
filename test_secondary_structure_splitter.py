""" This program is designed to test the functions of the secondary_structure_splitter """
import tempfile
import os
import pytest
from secondary_structure_splitter import get_fasta_lists, _verify_lists, output_results_to_files

# Sample FASTA data for testing
SAMPLE_FASTA = ">header1\n ATGC\n >header2\n ATGC"

def test_get_fasta_lists():
    """ Creating a temporary file with FASTA data """
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_fasta:
        temp_fasta.write(">header1\nATGC\n>header2\nATGC")
        temp_fasta.close()

        # Now pass the path of this temporary file to get_fasta_lists
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

def test_output_results_to_files():
    """ Test that output_results_to_files correctly writes to files """
    headers = ['>header1', '>header2']
    sequences = ['ATGC', 'ATGC']
    protein_output = 'test_protein.fasta'
    ss_output = 'test_ss.fasta'

    output_results_to_files(headers, sequences, protein_output, ss_output)

    # Clean up
    os.remove(protein_output)
    os.remove(ss_output)
