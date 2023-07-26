import pandas as pd
import getopt, sys

def process_genomic_data(input_file, result_file):

## Transforming genomic data of the species Lactococcus Lactis into a dataframe to use the pandas library
	df = pd.read_table(input_file, sep="\t")

## Filtering the columns of interest 
	df_iso_source = df[df["Assembly BioSample Attribute Name"] == "isolation_source"]
	df_env_medium = df[df["Assembly BioSample Attribute Name"] == "env_medium"]
	df_env_local_scale = df[df["Assembly BioSample Attribute Name"] == "env_local_scale"]
	df_geo_loc_name = df[df["Assembly BioSample Attribute Name"] == "geo_loc_name"]

## Renaming the columns Assembly BioSample Attribute Value to env_medium, isolation_source, env_local_scale and geo_loc_name
## respectively for each dataframe

	df_env_medium = df_env_medium.rename(columns={'Assembly BioSample Attribute Value': 'env_medium'})
	df_iso_source = df_iso_source.rename(columns={'Assembly BioSample Attribute Value': 'isolation_source'})
	df_env_local_scale = df_env_local_scale.rename(columns={'Assembly BioSample Attribute Value': 'env_local_scale'})
	df_geo_loc_name = df_geo_loc_name.rename(columns={'Assembly BioSample Attribute Value': 'geo_loc_name'})

 
## Setting the index as "Assembly Accession for each created dataframe

	df_iso_source = df_iso_source.set_index("Assembly Accession")
	df_env_medium = df_env_medium.set_index("Assembly Accession")
	df_env_local_scale = df_env_local_scale.set_index("Assembly Accession")
	df_geo_loc_name = df_geo_loc_name.set_index("Assembly Accession")

## Creating a list of columns including the additional columns : env_medium, env_local_scale and geo_loc_name
	columns = df_iso_source.columns.tolist()
	columns.append("env_medium")
	columns.append("env_local_scale")
	columns.append("geo_loc_name")

## Combining dataframes in order to merge the columns

	df_merge = df_iso_source.combine_first(df_env_medium).reindex(columns, axis=1)
	df2_merge = df_merge.combine_first(df_env_local_scale).reindex(columns, axis=1)
	df_merge_final = df2_merge.combine_first(df_geo_loc_name).reindex(columns, axis=1)

## Resetting the index "Assembly Accession"
	df_merge_final.reset_index(inplace=True)

## Filling missing values with "-"
	df_merge_final.fillna("-", inplace=True)

## Dropping the column "Assembly BioSample Attribute Name"

	df_merge_final.drop(["Assembly BioSample Attribute Name"], axis=1, inplace=True)

## Selecting the desired columns for the final output file

	df_merge_final = df_merge_final[["Assembly Accession","Source Database", "Assembly Assembly Method", "Assembly Stats Genome Coverage",
                "Assembly Stats Total Number of Chromosomes", "Assembly Stats Number of Scaffolds",
                "Assembly Stats Scaffold N50", "CheckM completeness", "CheckM contamination",
                "Assembly BioSample Accession", "Assembly BioSample Description Organism Common Name",
                "Assembly BioSample Description Organism Infraspecific Names Strain",
                "Organism Infraspecific Names Isolate", "Organism Infraspecific Names Strain", "isolation_source", "env_medium", "env_local_scale", "geo_loc_name",
                "Assembly BioSample Owner Name", "Assembly Submitter", "WGS project accession"]]

## Saving the results to a CSV file using tab as a separator

	df_merge_final.to_csv(result_file, sep="\t", index=False)



def get_missing_accessions(input_file, result_file, output_file): ## result_file is the same file that we obtained from the first function.
## Reading the file result_file
	df_fichier_res3 = pd.read_table(result_file)

## Reading the file input_file that contains the genomic data of the species lactococcus lactis
	df_l_lactis_metadata = pd.read_table(input_file, delimiter="\t")

## Storing the accession number in variables for each file
	fichier_res3_accessions = set(df_fichier_res3["Assembly Accession"])
	l_lactis_metadata_accessions = set(df_l_lactis_metadata["Assembly Accession"])
## Retrieving the missing accession numbers from input_file
	missing_accessions = l_lactis_metadata_accessions - fichier_res3_accessions
## Retrieving the missing rows (accession numbers and the other columns) by comparing the input_file (lactococcus lactis genomes) with the list of missing accession numbers
	missing_rows = df_l_lactis_metadata[df_l_lactis_metadata["Assembly Accession"].isin(missing_accessions)].drop_duplicates(subset="Assembly Accession", keep="first")

## Merging the missing rows with the result_file
	df_fichier_final = pd.concat([df_fichier_res3, missing_rows])

## Filling missing values with "-"
	df_fichier_final["env_local_scale"] = df_fichier_final["env_local_scale"].fillna("-")
	df_fichier_final["env_medium"] = df_fichier_final["env_medium"].fillna("-")
	df_fichier_final["geo_loc_name"] = df_fichier_final["geo_loc_name"].fillna("-")
	df_fichier_final["isolation_source"] = df_fichier_final["isolation_source"].fillna("-")

## Dropping the last two columns
	df_fichier_final = df_fichier_final.iloc[:, :-2]

## Saving the final file as CSV
	df_fichier_final.to_csv(output_file, sep='\t', index=False)
	

## Developpment of the input and output commands for the python script

def main(args) :
	input_file = None
	output_file = None
	

	
	try :
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:", ["help", "input=", "output="])
	except getopt.GetoptError:
		print("Usage: script.py -i <input_file> -o <output_file>")
		sys.exit(2)
	
	for opt,arg in opts :
		if opt == "-h" or opt == "--help":
			print("Usage: script.py -i <input_file> -o <output_file>")
			sys.exit()
		elif opt in ("-i", "--input"):
			input_file = arg
		elif opt in ("-o", "--output"):
			output_file = arg

	
	if input_file is None or output_file is None:
		print("Please specify the input and the output files using the -i and -o commands")
	
	process_genomic_data(input_file,output_file)
	get_missing_accessions(input_file, output_file,output_file)
	
if __name__ == "__main__" :
	main(sys.argv[1:])


