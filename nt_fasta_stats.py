""" This program is designed to generate two output files with the
pdb_protein.fasta file and pdb_ss.fasta file """
import sys
import argparse


def get_fasta_lists(file_path):
    """Parses a FASTA file and returns two lists: one for headers and one for sequences."""
    headers = []
    sequences = []

    with open(file_path, 'r', encoding='utf-8') as file:
        current_header = None
        current_sequence = ""

        for line in file:
            line = line.strip()

            if line.startswith('>'):
                if current_header is not None:
                    headers.append(current_header)
                    sequences.append(current_sequence)
                current_header = line
                current_sequence = ""
            else:
                current_sequence += line

        if current_header is not None:
            headers.append(current_header)
            sequences.append(current_sequence)

    return headers, sequences

def _verify_lists(header_list, sequence_list):
    if len(header_list) != len(sequence_list):
        sys.exit("Error: Header and sequence lists have different lengths")

def _get_num_nucleotides(nucleotide, sequence):
    if nucleotide not in ['A', 'G', 'C', 'T', 'N']:
        sys.exit("Invalid nucleotide code")
    return sequence.count(nucleotide)

def _get_ncbi_accession(header):
    return header.split()[0]

def print_sequence_stats(header_list, sequence_list, outfile_name):
    """ Defining function variable """
    _verify_lists(header_list, sequence_list)

    with open(outfile_name, 'w', encoding='utf-8') as outfile:
        outfile.write("Header\tNCBI Accession\tA_count\tG_count\tC_count\tT_count\tN_count\n")

        for header, sequence in zip(header_list, sequence_list):
            accession_string = _get_ncbi_accession(header)
            a_count = _get_num_nucleotides('A', sequence)
            g_count = _get_num_nucleotides('G', sequence)
            c_count = _get_num_nucleotides('C', sequence)
            t_count = _get_num_nucleotides('T', sequence)
            n_count = _get_num_nucleotides('N', sequence)

            outfile.write(f"{header}\t{accession_string}\t{a_count}\
            t{g_count}\t{c_count}\t{t_count}\t{n_count}\n")

def main():  # pragma: no cover
    """ Defining the main argument """
    parser = argparse.ArgumentParser(
        description='Provide a FASTA file to generate nucleotide statistics')
    parser.add_argument('-i', '--infile', dest='infile',
                        help='Path to the file to open', required=True)
    parser.add_argument('-o', '--outfile', dest='outfile',
                        help='Path to the file to write to', required=True)
    args = parser.parse_args()
    try:
        headers, sequences = get_fasta_lists(args.infile)
        _verify_lists(headers, sequences)

        # Assuming the output file is named based on the input file, with a suffix for the stats
        output_file = args.infile.rsplit('.', 1)[0] + '_stats.txt'
        print_sequence_stats(headers, sequences, output_file)

    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':  # pragma: no cover
    main()
