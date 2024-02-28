""" This program is designed to work with FASTA data and generate two separate files consisting of
the header and sequence respectively. """

# Importing modules
import sys
import argparse


"""Defining function variable 'get_fasta_lists' to return list of
header and sequence respectively."""


def get_fasta_lists(file_path):
    """ Defining a function variable called get_fasta_lists """
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


def output_results_to_files(header_list, sequence_list, protein_output_file, ss_output_file):
    """ Defining function variable to obtain output_file """
    with (open(protein_output_file, 'w', encoding='utf-8') as protein_file,
          open(ss_output_file, 'w', encoding='utf-8') as ss_file):
        for header, sequence in zip(header_list, sequence_list):
            if 'amino acid sequence' in header:
                protein_file.write(f"{header}\n{sequence}\n")
            else:
                ss_file.write(f"{header}\n{sequence}\n")


def main():
    """ Defining the program arguments """
    # Using the argparse to accept command line arguments.
    parser = argparse.ArgumentParser(
        description='Provide a FASTA file to perform splitting on sequence and secondary structure.')
    parser.add_argument('-i', '--infile', dest='infile', required=True, help='Path to file to open')
    args = parser.parse_args()
    try:
        headers, sequences = get_fasta_lists(args.infile)
        _verify_lists(headers, sequences)

        protein_output = 'pdb_protein.fasta'
        ss_output = 'pdb_ss.fasta'

        output_results_to_files(headers, sequences, protein_output, ss_output)

        print(f"Found {len(headers)} protein sequences")
        print(f"Found {len(sequences)} ss sequences", file=sys.stderr)

    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
