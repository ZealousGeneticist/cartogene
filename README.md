# cartogene
An Python program for taking chemicals and finding the genes they interact with and the mechanisms of interaction.

# Installation Instructions
git clone https://github.com/ZealousGeneticist/cartogene.git

# User Guide (alpha ver.)
Put the chemicals you want to analyze in the text file bioactive.tsv as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix. 

Then you can run the program on the chemicals by running this command in the terminal:

python cartogene_standalone_v1-2.py

Your final list should be in another text file called faceted_inact_node_network.tsv

# Alpha Branch Memo
This program isn't 100% finished, at all. Part of what is being completed is documentation for how to use the program for your own purposes. Before this Alpha branch gets merged in, this message should no longer be relevant!