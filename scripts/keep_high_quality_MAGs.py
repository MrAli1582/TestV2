#!/usr/bin/python
# -*- coding: <encoding name> -*-

import pandas as pd
import getopt
import sys
import os

## Function to filter MAGs based on their percent of contamination and completeness
def Filter_MAGs(input_file, output_file, directory):
    data = pd.read_table(input_file, sep='\t')
    
    filtered_data = data.copy()

    filtered_data = filtered_data[(filtered_data['Completeness'] > 85) & (filtered_data['Contamination'] < 5)]
     
    ## Creating a column path that contains the path of each MAG
    filtered_data['Path'] = filtered_data['Name'].apply(lambda x: os.path.join(directory, x + '') if pd.notnull(x) else None)
    ## Creating a second column full name that contains the full name of each MAG
    filtered_data['Full Name'] = filtered_data['Name'].str[:-3]
    ## Keeping both of the columns on the DataFrame
    filtered_data = filtered_data[['Path', 'Full Name']]

    filtered_data.to_csv(output_file, sep='\t', index=False, header=False)
 

## Function to define and parse script options   
def main(argv):
    input_file = None
    output_file = None
    directory = None

    try:
        opts, args = getopt.getopt(argv, "hi:o:d:", ["help", "input=", "output=", "directory="])
    except getopt.GetoptError:
        print("Usage: script.py -i <input_file> -o <output_file> -d <directory>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
            print("Usage: script.py -i <input_file> -o <output_file> -d <directory>")
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-d", "--directory"):
            directory = arg

    if input_file is None or output_file is None or directory is None:
        print("Please specify the input file, output file, and directory using the -i, -o, and -d options")

    Filter_MAGs(input_file, output_file, directory)


if __name__ == "__main__":
    main(sys.argv[1:])
