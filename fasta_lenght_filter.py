import sys
import os
# usage: python fasta_length_filter.py  test.fasta   150 

fo_1 = sys.argv[1].strip().split(".fa")[0] + "-%s"%(str(sys.argv[2]))  +  "-filtered.fa"
os.system('rm -rf %s'%(fo_1))
for ele in open(sys.argv[1],"r").read().strip().split(">")[1:] :
    name = ele.strip().split("\n")[0]
    seq = "".join(ele.strip().split("\n")[1:])
    if len(seq) > int(sys.argv[2]) : 
        with open(fo_1 , "a+") as f:
            f.write(">" + str(name.strip()) + "\n" + seq.strip() + "\n")


