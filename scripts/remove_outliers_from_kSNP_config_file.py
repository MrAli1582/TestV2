
import getopt
import sys
import os

## Function to remove the  genome outliers from the kSNP configuration file
def remove_lines(input_file, intermediate_file, output_file):
	## First, opening and reading the file that contains the genome outliers
    with open(input_file, 'r') as f1:
        values_to_remove = set(line.strip() for line in f1)
   
    # Opening the kSNP configuration file that contains all the genomes and removing those who were found in the input file
    with open(intermediate_file, 'r') as f2, open(output_file, 'w') as out:
        for line in f2:
            if line.strip().split()[1] not in values_to_remove:
                out.write(line)
## Function to define and parse script options using argparse    
def main(argv):
    input_file = None
    intermediate_file = None
    output_file = None

    try:
        opts, args = getopt.getopt(argv, "hi:m:o:", ["help", "input=", "mid=", "output="])
    except getopt.GetoptError:
        print("Usage: script.py -i <input_file> -m <intermediate_file> -o <output_file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            print("Usage: script.py -i <input_file> -m <intermediate_file> -o <output_file>")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-m", "--intermediate"):
            intermediate_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
       

    if input_file is None or intermediate_file is None or output_file is None:
        print("Please specify the input file, intermediate file, and the output file using the -i, -m, and -o options")

    remove_lines(input_file, intermediate_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
