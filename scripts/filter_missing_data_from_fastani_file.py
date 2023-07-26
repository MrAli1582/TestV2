import argparse

## Function to extract the assembly accession ID from the given genome name 
def extract_genome_id(genome_name):
    if genome_name.startswith("GCA_") or genome_name.startswith("GCF_"):
       ## return the first two parts of the accession name separated by "_"
        return "_".join(genome_name.split("_")[:2])
		
    elif genome_name.startswith("MAG_"):
       ## If the line contains a MAG, remove the _fa extension and keep the rest
        return genome_name.split("_fa")[0]		
        
    else:
       ## Otherwise, return the genome name as it is
        return genome_name

## Function to filter unique genomes from the input_file

def filter_unique_genomes(input_file, output_file):
	
    genome_counts = {}
    
    ## Read the input file and count the occurences of each genome's assembly accession ID
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip() 
            genome_name1, _ = line.split("\t", 1)
            genome_id = extract_genome_id(genome_name1)
            genome_counts[genome_id] = genome_counts.get(genome_id, 0) + 1

    ## Writing the IDs that verify the condition in a new file
    with open(output_file, "w") as f:
        for genome_id, count in genome_counts.items():
            if count == 1:
                f.write(genome_id + "\n")

## Defining and parsing the script options using argparse

def define_script_options():
    parser = argparse.ArgumentParser(description='Script to filter unique genomes from the input file.')
    parser.add_argument('-i', '--input', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output file', required=True)

    return parser.parse_args()

if __name__ == "__main__":
    args = define_script_options()

    filter_unique_genomes(args.input, args.output)
