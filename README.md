# cartogene
An Python program for taking chemicals and finding the genes they interact with and the mechanisms of interaction.

# Installation Instructions
git clone https://github.com/ZealousGeneticist/cartogene.git

## User Guide
Put the chemicals you want to analyze in the text file bioactive.tsv as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix. 

Then you can run the program on the chemicals by running this command in the terminal (given you have python3 installed and pip installed):

python3 cartogene_standalone_v1-2.py -i <your_chem_file>

Your final list should be in another text file called <faceted_inact_node_network.tsv>, unless you wish to name it something else, in which case you simply add -o <my_output> to the above command and it will come out as <my_output.tsv> .

### Advanced User Guide
Here is the entire list of optional commands that can be utilized for cartogene: 
+ **Input File**
    + "-i", "--input"
    + **ONLY REQUIRED ARGUMENT**
    + *Description*: This is the one required argument for the program which feeds the chemical list from the file into the script. This is the full name of the file.
        + As stated above; put the chemicals you want to analyze in the text file bioactive.tsv as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix.
+ **Edge List File Name**
    +"-o", "--output"
    + *Description*: This is the final name of your edge list file. No alterations are made to this final name, so you may label it as any file type you wish (.tsv is suggested). By default, the name is set to <faceted_inact_node_network.tsv>
+ **CTD Chemical-Gene Interaction Table File Name**
    +"-c", "--ctd"
    + *Description*: This is the name for the intermediate Comparative Toxicogenomics Database (CTD) chemical-gene interaction table file. You can put in a name like -i or -o , however this final file name will have the suffix '_chemical-protein.tsv' added to it. By default, the name is `interactionsCTD`, which makes the final product <interactionsCTD_chemical-protein.tsv>
+ **IntAct Intermediate Data File Name**
    + "-j", "--json"
    + *Description*: This is the name for the intermediate IntAct gene-gene interaction JSON data file *prefix*. When any files are being made they have a file number for order like this: `_#_PPI.json` (unless running --test True). By default, the name is `faceted_intact_results`, which means the final name(s) is/are <faceted_intact_results_#_PPI.json>
        + *This file is extremely large for the JSON data type and can make most viewers stall significantly or even crash. If you wish to view it anyways, check the --removejson documentation below.* 
+ **NCBI Organism Taxonomy Number**
    + "-g", "--organism"
    + *Integer value*
    + *Description*: This integer value is the ID for the organism you wish to search by. By default, it uses the one for humans (`9606`).
+ **Omniscience Specific Single-Data-File Tester**
    + "-t", "--test"
    + *Bool value*
    + *Description*: This bool value is used to output only one IntAct JSON to test computing problems on weaker hardware. By default, it is `False` and doesn't affect anything.
+ **Debug**
    + "-d", "--debug"
    + *Bool value*
    + *Description*: This bool value is used to activate debug mode. This is primary used by the developers to figure out why some code is messing up and where in the script. It is by default `False` and off.
+ **Remove Intermediate IntAct Data JSON**
    + "-r", "--removejson"
    + *Bool value*
    + *Description*: This bool value is used to turn on or off the cleanup() process in the script which removes the chunky IntAct JSON, as normally the JSON is to large for any convient use on the user's end after it has been used by the program. It is **by default** `True` and **turned on.**
+ **Edge List Header Enable/Disable**
    + "-e", "--header"
    + *Bool value*
    + *Description*: This bool value is used as a way to control whether you wish for the final output file to have headers for the edge list or to only have the columns be data. It is **by default** `True` and as such **keeps the headers**.

## Memo
This program isn't 100% finished, at all. Part of what is being completed is documentation for how to use the program for your own purposes. Before this Alpha branch gets merged in, this message should no longer be relevant!