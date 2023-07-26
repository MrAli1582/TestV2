
Please make sure to read this file before launching the workflow!

## In your python environment, don't forget to install pandas and Biopython. (using pip install pandas and pip install Biopython)


## Before launching the workflow, make sure that you search for the genome representative of the species that you want to analyze using :

https://www.ncbi.nlm.nih.gov/assembly

## First search the name of the species, then to your left, look for Representative in the Refseq Category section.

## Make sure that the name of the original MAGs files ends with a .fa extension, because otherwise the workflow wouldn't work!

## Also make sure to change the different pathways on the configuration file so that the workflow works on your own environment.



Important!!




## Please note that for the dRep tool, if you get the following error during the MASH step :



pivot() takes 1 argument but 4 were given




It's caused by the fact that pandas was upgraded without updating dRep.

SO make sure that you upgrade pandas AND dRep to the latest version!! 

using the following commands:

pip install pandas --upgrade

pip install dRep --upgrade


## if you face any other sort of problems, please contact the developer of the dRep tool via Github.








## Note that if you want to download the genomes that take part of the Refseq database, don't forget to change the genomes source for the first step of the workflow on the YAML configuration file!

## Also the name of the genome reference to filter the outlier genomes! (GCF for Refseq and GCA for Genbank)





## Here is the command that launches the snakemake workflow to study MAGs of a species :

qsub -cwd -V -N test_carnosum -pe thread 4 -q long.q -b y "conda activate snakemake-6.9.1 && snakemake --snakefile /save_home/ayouncha/MesScripts/phylogenomic_study_of_MAGs_script  --configfile /home/ayouncha/save/MesScripts/l_carnosum.yaml --printshellcmds --jobs 100 --restart-times 5 --latency-wait 60  --use-conda --cluster 'qsub -V -cwd -R y -N {rule} -pe thread {threads} -q {params.queue} -e [LOG_DIR] -o [LOG_DIR]'  &&  conda deactivate"

