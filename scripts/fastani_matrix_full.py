import csv
import pandas as pd
from collections import defaultdict
import getopt
import sys
from Bio import Phylo

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:o:n:rd', ["help", "input=", "output=", "newicktree=","reverttodistances", "divideper100"])
    except getopt.GetoptError as err:
    # print help information and exit:
        print (str(err)) 
        usage()
        sys.exit(2)
    inputFileName = None
    newickTreeFileName = None
    outputFileName = './matrix.out.csv'
    revert_matrix_values = False
    divide_matrix_values_per_100 = False

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            inputFileName = a
        elif o in ("-o", "--output"):
            outputFileName = a
        elif o in ("-n", "--newicktree"):
            newickTreeFileName = a
        elif o in ("-r", "--reverttodistances"):
            revert_matrix_values = True
        elif o in ("-d", "--divideper100"):
            divide_matrix_values_per_100 = True
        else:
            assert False, "unhandled option"
            
    if(newickTreeFileName):
    # if a newick tree is provided (enter its path with the -n parameter) : record the leef order of this tree
        orderList = []
        with open(newickTreeFileName, 'r') as newick_tree_file:
            tree = Phylo.read(newickTreeFileName, "newick")
            tree.ladderize()
            for x in tree.get_terminals():
                 orderList.append(x.name)


    with open(inputFileName, 'r') as fast_ani_file:
        reader = csv.reader(fast_ani_file, delimiter = '\t')
        value = ""
        ani = defaultdict(dict)
        #1st pass to construct the matrix in memory
        for row in reader:
            if(divide_matrix_values_per_100):
                if(revert_matrix_values):
                    distance = round(float(1-(float(row[2])/100)), 2)
                    seuil = round(float(0.3000),2)
                else:
                     distance = round(float(row[2])/100, 2)
                     seuil = round(float(0.7000),2)
            else:
                if(revert_matrix_values):
                    distance = round(float(100-float(row[2])), 2)
                    seuil = round(float(30),2)
                else:
                     distance = round(float(row[2]), 2)
                     seuil = round(float(70),2)
            ani[row[0]][row[1]] = distance
            ani[row[1]][row[0]] = distance		
            #print("--\trow0:"+row[0]+"--\trow1:"+row[1]+"--\trow2:"+row[2])
            
    df = pd.DataFrame(ani).T.fillna(seuil)
    #if relevant: order the matrix with the clustering order of the semi matrix
    if(newickTreeFileName):
        df = df.loc[orderList, orderList]
    print('outputfileName:' + outputFileName)
    df.to_csv(outputFileName, index=True, sep='\t')

def usage():
    print ("USAGE: python fastani2matrix.py  [-h] [-r] [-d] [-i <FastANIInputFileName>] [-o <MatrixOutputFileName>] [-m <SemiMatrixFromFastANIInputFileName>] ")

if __name__ == "__main__":
    main()
