# Calculating statistics from a fastq file

The script parse_fastq.py calculates the following statistics from a fastq file:

- Number of reads

- Mean length of the reads

- GC mean percentage 

- doublet frequency of the two first bases

Before running the script, you must install the packages argparse, re, numpy and matplotlib (pip or conda)

- To run, an example:

        python parse_fastq.py fastq_files/TESTX_H7YRLADXX_S1_L001_R1_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L001_R2_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L002_R1_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L002_R2_001.fastq

I have written another script parse_fastq_with_graphs, which is quite the same as parse_fastq.py but this one shows a final plot of the number of reads, mean length of reads and GC percentage. It can be useful to compare sample results. You have to pass at least two samples to have the plots, otherwise you'll get the same result as parse_fastq.py. To run, you just have to change the name of the script in the previous command line.