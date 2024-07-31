#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 14:55:50 2024

@author: richapatel
"""

import subprocess

def run_get_complete(graph_file, complete_dir):
    try:
        print("Running GetComplete...")
        subprocess.run(['get_organelle_from_assembly.py', '-F', 'animal_mt', '-g', graph_file, '-o', complete_dir, '--no-slim'], check=True)
        print("GetOrganelle completed successfully.")
    except subprocess.CalledProcessError as e: #if an error occurs
        print(f"Error running Get Complete: {e}")

#just need to change the filename, refrence, and output_dir here in order to run the script.
def main():
    # Define file names
    graph_file = "animal_mt.K105.contigs.graph1.selected_graph.gfa"
    complete_dir = "fish_assembly_complete"

# Run the commands
    run_get_complete(graph_file, complete_dir)

if __name__ == '__main__':
    main()
