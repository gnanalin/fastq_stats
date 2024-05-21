"""Parse a fastq file and calculate some statistics."""

import argparse
import os
import re
import matplotlib.pyplot as plt
import numpy as np


def check_file(fastq_file):
    """Check whether the path exists.

    Parameters
    ----------
    fastq_file : the path of the fastq file

    Retuns
    ------
    bool : True if the path exists
    """
    if os.path.exists(fastq_file):
        print(f"The file {fastq_file} is going to be analysed...")
        return True
    else:
        print("The file does not exists !")
        return False


def parse_arguments():
    """Return the path of the fastq files.

    Parameters
    ----------
    -h : for help
    fastq : the path of the fastq files separated with space

    Returns
    -------
    str : the path of the fastq file
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("fastq", nargs="+", type=str ,help="pass your fastq files path separated with space")
    args = parser.parse_args()
    return args.fastq


def calculates_stats(fastq_file):
    """Calculate statistics on a fastq file.

    Parameters:
    -----------
    fastq_file : the fastq file on which to calculate the stats

    Returns:
    --------
    None : prints the result
    """
    # I initialize some variables to store the results of the stats
    total_reads = 0
    reads_length = 0
    # I decided to use a boolean in order to not consider the quality scores as part of the sequence read.
    # Once I have found a +, I know that the next line is going to be the quality scores, so I put the flag to False.
    # So when the flag is False, it means that I am reading the read sequence so I append the length to the corresponding variable.
    find_plus = False
    gc_proportion = 0
    two_first_bases = {}
    with open(fastq_file, "r") as fr:
        for line in fr:
            line = line.strip()
            # Just below, I use a regular expression in order to have a more generalized script for different fastq files from different sequencing technologies.
            # However, in this case, I could have just done : line.startswith("@HISEQ")
            if re.match("@[A-Z].*:[0-9].*:.*:[0-9].*:[0-9].*:[0-9].*:[0-9].*", line):
                total_reads += 1
            elif line == "+":
                find_plus = True
            elif not find_plus:
                two_first_letters = line[0:2]
                # I use the get method because there are a lot of doublet possibilities in order to count them.
                # If I have a new key, then it will be added to the dictionnary. If I already have the key, it will just increment the count.
                two_first_bases[two_first_letters] = two_first_bases.get(two_first_letters, 0)+1
                read_length = len(line)
                reads_length += read_length
                # In order to count the GC proportion, I used the method count.
                gc_proportion += ((line.count("G")+line.count("C"))/read_length)*100
            else:
                find_plus = False

    mean_reads_length = round(reads_length/total_reads, 2)
    mean_gc_proportion = round(gc_proportion/total_reads, 2)
    # To print the results, I use f-strings.
    print(f"There are {str(total_reads)} reads in the sample.")
    print(f"The mean length of the reads is {str(mean_reads_length)} bases.")  # I also normalize the reads length to get a mean.
    print(f"The mean GC percentage is {str(mean_gc_proportion)}%")  # As for the GC proportion.
    print("Doublet frequency for the first two bases of each read :")
    for k, v in two_first_bases.items():
        print(f"{k} -> {str(v/total_reads)}")
    return [total_reads, mean_reads_length, mean_gc_proportion]


def plot_results(file_names, stats_np):
    """Plot total number of reads, mean read length and mean GC proportion for each sample.

    Parameters:
    -----------
    file_names : the fastq file names

    Returns:
    --------
    None : prints the bar plots
    """
    fig,(ax1,ax2,ax3) = plt.subplots(1,3, figsize=(5*len(stats_np), 6))
    bar1 = ax1.bar(file_names, stats_np[:,0], color="green")
    ax1.set_title("Total number of reads")
    bar2 = ax2.bar(file_names, stats_np[:,1],color="blue")
    ax2.set_title("Mean read length")
    bar3 = ax3.bar(file_names, stats_np[:,2],color="red")
    ax3.set_title("Mean GC proportion")
    ax1.set_xticks(range(len(file_names)))
    ax2.set_xticks(range(len(file_names)))
    ax3.set_xticks(range(len(file_names)))
    ax1.set_xticklabels(file_names, rotation=45, ha='right', fontsize=7)
    ax2.set_xticklabels(file_names, rotation=45, ha='right', fontsize=7)
    ax3.set_xticklabels(file_names, rotation=45, ha='right', fontsize=7)
    ax1.bar_label(bar1)
    ax2.bar_label(bar2)
    ax3.bar_label(bar3)
    plt.tight_layout() 
    plt.show()
    
if __name__ == '__main__':
    # parsing the arguments
    fastq_files = parse_arguments()
    concat_stats = []
    file_names = []
    for fastq_file in fastq_files:
        # checking the existance of the file
        if check_file(fastq_file):
            # calculating the statistics
            file_names.append(fastq_file)
            stats = calculates_stats(fastq_file)
            concat_stats.append(stats)
    concat_stats_np = np.array(concat_stats)
    if len(file_names) > 1:
        # In order to compare results from different samples, plotting the results can be useful.
        # I decide to plot the results only if there are at least two samples.
        plot_results(file_names, concat_stats_np)
    