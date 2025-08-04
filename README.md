# FishMitogenomeAssembly

**Acknowledgements**

This project is based on MitogenomeAssemblyPipeline (https://github.com/rozgaw/MitogenomeAssemblyPipeline). Many thanks to the original author(s) for their work.

**Dependencies**
- SRA toolkit https://github.com/ncbi/sra-tools
- FastQC https://github.com/s-andrews/FastQC
  - conda install bioconda::fastqc
- fastp https://github.com/OpenGene/fastp
  - conda install bioconda::fastp
- GetOrganelle https://github.com/Kinggerm/GetOrganelle

**Python Packages**
- subprocess 

# Assembly Steps

## Download SRA FASTQ files
1. Make sure you have the SRA toolkit installed.
2. In the terminal run: "prefetch [SRA ID]"
   - In our case, we ran: `prefetch SRR15139196`
3. Next, to split the paired end reads run: `fastq-dump -I --split-files SRR15139196`
   - This should leave you with two fastq files. One "[SRA ID]_1.fastq" for the forward read and the other "[SRA ID]_2.fastq" for the reverse read.
   - In our case, the files are "SRR15139196_1.fastq" and "SRR15139196_2.fastq".

## Evaluate read quality using FastQC
1. **Input:** Raw sequencing data: FASTQ files.
2. **Command (in terminal):** `fastqc SRR15139196_1.fastq SRR15139196_2.fastq`
3. **Output:** Summary graphs and tables to help assess read quality.
4. To look at the visualizations in FastQC:
   - `open SRR15139196_1_fastqc.html`
   - `open SRR15139196_2_fastqc.html`
   - This opens the HTML files in your browser to view the visualizations.

## Trim sequences using fastp
1. **Input:** Raw sequencing data: FASTQ files.
2. **Command:** 
   - `fastp -i SRR15139196_1.fastq -I SRR15139196_2.fastq -o out.SRR15139196_1.fastq -O out.SRR15139196_2.fastq`
   - Command to trim adaptors only (No quality trimming): `fastp -i SRR15139196_1.fastq -I SRR15139196_2.fastq -o out.SRR15139196_1.fastq -O out.SRR15139196_2.fastq -Q`
3. **Output:** Trimmed fastq files "out.SRR15139196_1.fastq" and "out.SRR15139196_2.fastq".

## Assemble the mitogenome using GetOrganelle
1. Use the following page for download instructions: [GetOrganelle Installation](https://github.com/Kinggerm/GetOrganelle/wiki/Installation#installation)
2. **Input:** Adaptor trimmed fastq files (out.SRR15139196_1.fastq, out.SRR15139196_2.fastq) and seed sequence (GenBank accession no. HQ338402, ND2 gene fasta file).
3. **Command:**
   - `get_organelle_from_reads.py -s ND2.fasta -1 out.SRR15139196_1.fastq -2 out.SRR15139196_2.fastq -R 10 -k 21,45,65,85,105 -F animal_mt -o fish_assembly`
4. **Output:**
    - *.path_sequence.fasta, each fasta file is an assembled genome.
    - *.selected_graph.gfa, the organelle-only assembly graph.
    - get_org.log.txt, the log file.
    - extended_K*.assembly_graph.fastg, the raw assembly graph.
    - extended_K*.assembly_graph.fastg.extend_embplant_pt-embplant_mt.fastg, a simplified assembly graph.
    - extended_K*.assembly_graph.fastg.extend_embplant_pt-embplant_mt.csv, a tab-format contig label file for bandage visualization.
    - The most important file is the ***.fasta** file and all of the other files can be deleted/ignored if the full genome is complete (you can find this information in the log file too).
    - If you get scaffolds/contigs as a result of the assembly (which was the case for this assembly), you will need to complete the assembly using the `GetComplete.py` file. See below for details.

## Annotate the assembled genome using MitoZ
- Annotation is not automatically done by the pipeline, but this is how to generate it using MitoZ.
1. First, ensure that MitoZ and its dependencies are downloaded. Visit https://github.com/linzhi2013/MitoZ for details.
2. Since we are not using it for assembly, just annotation, we will use the -annotate- subcommand. The subcommand requires the following for best performance:
    - `--fastafile:` Path to .fasta file. In our case, this is where the completed GetOrganelle assembly is.
    - `--outprefix:` Prefix to new directory that will contain output
    - `--genetic_code:` Specifies the translation table and which NCBI genetic code to use. We use "2" to specify vertebrates, as that is what we are working with.
    - `--clade:` Specifies the taxonomic context. We use "Chordata" to specify vertebrates, as that is what we are working with.
    - **Command:**
      - `mitoz annotate --fastafile GetOrganelleMitogenomeAssemblyFAga.fasta --outprefix NEW_annot --genetic_code 2 --clade Chordata`

## Visualize the assembled genome using MitoFish (MitoAnnotator)
1. Visit: [MitoFish](https://mitofish.aori.u-tokyo.ac.jp/)
2. **Input:** Mitogenome file in FASTA format.
    - Needs to be less than 100 Kb.
    - Note if DNA is circular (complete).
    - Note if visualization is desired (slower run time).
3. **Output:** Download the files from MitoAnnotator, it only keeps them on the server for 10 days.
    - Annotation.pdf (visualization).
    - genes.fasta.
    - raw.fasta.
    - NCBI.txt.
    - Annotation.txt.

# Finding a Seed Sequence
1. Search fish scientific name in NCBI Nucleotide database (https://www.ncbi.nlm.nih.gov/nucleotide/)
2. Find a mitochondrial gene/sequence (can be partial)
3. Download the sequence as a .fasta file.
4. Rename file accordingly (if desired)

# Using EditedPipeline.py File
- Make sure that the dependencies are installed and working 
- Make sure that the getorganelle environment is activated
- Before running the python file, change the file names accordingly in the main() function.
  - **filename:** name of the SRR file that you want to grab from the SRA database
  - **forward & reverse:** when you run the run_splitends() function, the output will automatically be named into SRR_1.fastq & SRR_2.fastq. Make sure to follow this format when declaring these file names.
  - **out_forward & out_reverse:** desired filenames for output trimmed files from run_fastp() function. Naming convention followed is: out.SRR_1.fastq & out.SRR_2.fastq.
  - **reference:** Name of seed sequence fasta file
  - **output_dir:** Name of output directory that will be created containing the mitogenome assembly.
- Run the file in the terminal
  - Command: `python3 EditedPipeline.py`
- NOTE: Only **filename, reference, and output_dir** need to be re-named as forward, reverse, out_forward, & out_reverse will be automatically formatted accordingly. They can be changed if desired. 


# Using GetComplete.py File 
- If the initial GetOrganelle run from reads leaves you with contigs/scaffold and not a complete mitogenome, run the GetComplete.py file.
- This process will need to be done in the output folder (output_dir) containing the contigs and assembly graph obtained previously.
- Make sure that the getorganelle environment is activated
  - Command: `conda activate getorganelle`
- Before running the python file, change the file names accordingly in the main() function. 
  - **graph_file:** Name of the *.gfa that contains the assembly graph, should be in output_dir
  - **assembly_dir:** Name of output directory that will be created containing the assembled contigs. 
- Run the file in the terminal
- Command: `python3 GetComplete.py`
- Output:
  - *.path_sequence.fasta, one fasta file represents one type of genome structure
  - *.fastg, the organelle related assembly graph to report for improvement and debug
  - *.selected_graph.gfa, the organelle-only assembly graph
  - get_org.log.txt, the log file
- The most important file is the **.fasta** sequence containing the completed assembly. This .fasta file is what you would use as the completed assembly and for further analysis.

# Comparing Assembled Mitogenome to Existing 
- If there is already a published mitogenome for the fish species of interest, you can compare the generated assembly against it to see accuracy. 
1. Use Align Sequences Nucleotide BLAST
   - https://blast.ncbi.nlm.nih.gov/Blast.cgi?BLAST_SPEC=blast2seq&LINK_LOC=align2seq&PAGE_TYPE=BlastSearch 
2. Under “Enter Query Sequence”, supply the reference genome accession number of FASTA file
3. Under  “Enter Subject Sequence,” supply the assembled genome FASTA file or copy and paste the sequence. 
4. Under “Program Selection” optimize for highly similar sequences (megablast)


