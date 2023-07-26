import argparse

## Function to filter genomes with ANI values below a threshold based on a reference genome
def filter_genomes_by_ani(input_file, output_file, reference_genome, threshold_ani):
    filtered_genomes = []
    ## Reading the input file and checking the ANI values for the reference genome
    with open(input_file, 'r') as f:
        for line in f:
            columns = line.strip().split()
            genome_ref = columns[0]
            genome_id = columns[1]
            ani_percentage = float(columns[2])
            ## Checking if the line contains the reference genome and if the ANI percent is less than the threshold
            if genome_ref == reference_genome and ani_percentage < threshold_ani:
                filtered_genomes.append(genome_id)
    ## Writing the assembly accession ID of the genomes that verify the condition to the output file
    with open(output_file, 'w') as f:
        for genome_id in filtered_genomes:
            f.write(genome_id + '\n')

## Function to define and parse script options using argparse            
def define_script_options():
    parser = argparse.ArgumentParser(description='Script to filter genomes with ANI values below a threshold.')
    parser.add_argument('-i', '--input', help='Path to the input file', required=True)
    parser.add_argument('-o', '--output', help='Path to the output file', required=True)
    parser.add_argument('-g', '--genome', help='ID of the reference genome', required=True)
    parser.add_argument('-t', '--threshold', help='Threshold value of ANI', default=95, type=float)

    return parser.parse_args()

if __name__ == "__main__":
    args = define_script_options()

    filter_genomes_by_ani(args.input, args.output, args.genome, args.threshold)
