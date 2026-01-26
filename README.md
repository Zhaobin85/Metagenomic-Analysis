This program is designed to perform the assembly and binning of the metagenomes of Spartina alterniflora root microbiomes, wich included trimming of the metagenomic reads, congtig assembly with megahit, MAGs grouping with metawrap, genome quality assessement with CheckM, etc.

###Step-by-step pipeline for the assembly and binning of the metagenomes.

Step 1. Raw reads trimming using Sickle
sickle pe -f A1.R1.raw.fastq.gz -r A1.R2.raw.fastq.gz -o A1.R1.trim.fastq -p A1.R2.trim.fastq -s A1.single.trim.fastq -l 50 -q 20 -t sanger 

2. Assembly and Co-assembly
For single sample:
megahit -1 A1.R1.trim.fastq -2 A1.R2.trim.fastq -o A1_assembly --min-contig-len 1000
For multiple samples:
megahit -1 A1.R1.trim.fastq,A2.R1.trim.fastq -2 A1.R2.trim.fastq,A2.R2.trim.fastq -o A1A2_assembly --min-contig-len 1000

3. Binning of the contigs
1) metawrap binning -o A1_INITIAL_BINNING -a A1.final.contigs.fa --metabat2 --maxbin2 --concoct A1_Clean_reads/A1_*.fastq -t 36
2) metawrap bin_refinement -o A1_BIN_REFINEMENT -A A1_INITIAL_BINNING/metabat2_bins -B A1_INITIAL_BINNING/maxbin2_bins -C A1_INITIAL_BINNING/concoct_bins -c 50 -x 10 -t 36
3) metawrap reassemble_bins -o A1_BIN_REASSEMBLY -1 A1_Clean_reads/*_1.fastq -2 A1_Clean_reads/*_2.fastq -m 96 -c 50 -x 10 -t 36 -b A1_BIN_REFINEMENT/metawrap_50_10_bins

4. Collecting the MAGs and Remove the contig length shorter than 1000 bp within each MAG
for f in *.fa;python fasta_length_filter.py "$f" 1000;done

5. Genome quality assessment
checkm lineage_wf -x fa --tab_table ./All_MAGs ./All_MAGs_Checkm -f All_MAGs.txt -t 36

###Calculation of the host DNA contamination

1. Index the host genome
$bowtie2-build GCA_008808055.3.fna S.alterniflora 

2. 
$bowtie2 -p 24 -1 A.R1.trim.fastq -2 A.R2.trim.fastq -x S.alterniflora --un-conc-gz ./A.dehost.R%.fastq.gz -S ./A.host.sam
