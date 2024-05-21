# Calculating statistics from a fastq file

This script calculates the following statistics from a fastq file:

- Number of reads

- Mean length of the reads

- GC mean percentage 

- doublet frequency of the two first bases

Before running the script, you must install the package argparse (pip or conda)

- To run, an example:

        python parse_fastq.py fastq_files/TESTX_H7YRLADXX_S1_L001_R1_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L001_R2_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L002_R1_001.fastq fastq_files/TESTX_H7YRLADXX_S1_L002_R2_001.fastq


There are some fastq files to test the script.