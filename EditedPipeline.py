#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:21:29 2024

@author: richapatel
"""

import subprocess
    
#runs the fetch data fuction of the code
def run_prefetch(filename):
    try: 
        print("Running prefetch...")
        subprocess.run(['prefetch', filename], check=True)
        print('Prefetch completed successfully.')
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running Prefet: {e}")
    
#runs the split-files function of the code
def run_splitends(filename):
    try: 
        print("Running split ends...")
        subprocess.run(['fastq-dump', '-I', '--split-files', filename], check=True)
        print('Split ends completed successfully.')
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running Prefet: {e}")   

#runs the fastqc function of the code
def run_fastqc(forward, reverse):
    try:
        print("Running FastQC...")
        subprocess.run(['fastqc', forward, reverse], check=True)
        print("FastQC completed successfully.")
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running FastQC: {e}")

#runs the fastp function of the code
def run_fastp(forward, reverse, out_forward, out_reverse):
    try:
        print("Running fastp...")
        subprocess.run(['fastp', '-i', forward, '-I', reverse, '-o', out_forward, '-O', out_reverse], check=True)
        print("fastp completed successfully.")
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running fastp: {e}")

#runs the gerorganelle function of the code
def run_get_organelle(reference, out_forward, out_reverse, output_dir):
    try:
        print("Running GetOrganelle...")
        subprocess.run(['get_organelle_from_reads.py', '-s', reference, '-1', out_forward, '-2', out_reverse, '-R', '10', '-k', '21,45,65,85,105', '-F', 'animal_mt', '-o', output_dir], check=True)
        print("GetOrganelle completed successfully.")
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running GetOrganelle: {e}")


#just need to change the filename, refrence (seed file name), and output_dir here in order to run the script.
def main():
    # Define file names
    filename = 'SRR15139196'
    forward = filename + '_1.fastq'
    reverse = filename + '_2.fastq'
    out_forward = 'out.' + filename +'_1.fastq'
    out_reverse = 'out.' + filename +'_2.fastq'
    reference = 'N2.fasta'
    output_dir = 'fish_assembly'

# Run the commands
    run_prefetch(filename)
    run_splitends(filename)
    run_fastqc(forward, reverse)
    run_fastp(forward, reverse, out_forward, out_reverse)
    run_get_organelle(reference, out_forward, out_reverse, output_dir)

if __name__ == '__main__':
    main()
