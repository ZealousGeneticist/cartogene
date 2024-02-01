# cartogene
A Python program for taking chemicals and finding the genes they interact with and the mechanisms of interaction.

# Installation Instructions
git clone https://github.com/ZealousGeneticist/cartogene.git

## User Guide
Put the chemicals you are wanting to analyze in the input text file (tutorial example: <bioactive.tsv>) as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix. *Make sure they are return- or |-delimited!*
+ The tutorial text file <bioactive.tsv> has been given to show multiple examples for how chemicals can be written. However, if you are unsure as to if your chemical is not showing up, check the Comparative Toxicogenomic Database to make sure it is there!

Then you can run the program on the chemicals by running this command in the terminal (given you have python3 installed and pip installed):

python3 cartogene_standalone.py -i <your_chem_file>

Your final list should be in another text file called <faceted_inact_node_network.tsv>, unless you wish to name it something else, in which case you simply add -o <my_output> to the above command and it will come out as <my_output> .

***If you are using a machine like a supercomputer where you do not have permissions to install packages to the python folder which are needed for this program, make sure to run this command after MANUALLY installing the required packages. A fix for this so you don't need to manually do that is coming soon for the less permissioned among your machines.***

**python3 cartogene_standalone.py -i <your_chem_file> -z**

------


#### Quick Guide on Networks
    Nodes: Think of nodes as individual points or entities. In a biological network, nodes could be genes or chemicals or proteins or all of the above.

    Edges: Edges represent connections or relationships between nodes. In a biological network, an edge could represent an interaction between genes or proteins or chemicals or any of the above.

    Networks: Networks are a collection of nodes and edges. When you have multiple chemicals/proteins/genes connected through interactions, you have a biological network.

    Communities: Communities are groups of nodes that are more densely connected to each other than to nodes outside the group. In a biological network, a community could be a group of proteins who interact more with each other (say, to make an enzyme) than with proteins outside the group.
So, nodes are individual data points, edges are connections between them, networks are the overall structure, and communities are tightly-knit groups within that structure.

------

### Advanced User Guide
Here are the optional commands that can be utilized for cartogene: 
+ **Input File**
    + "-i", "--input"
    + **ONLY REQUIRED ARGUMENT**
    + *Description*: This is the one required argument for the program which feeds the chemical list from the file into the script. This is the full name of the file.
        + As stated above; put the chemicals you want to analyze in the input text file (tutorial example: <bioactive.tsv>) as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix.
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
    + *Description*: This argument is used to output only one IntAct JSON to test computing problems on weaker hardware. By default, it is `False` and doesn't affect anything. Simply calling the argument changes it to `True`.
+ **Debug**
    + "-d", "--debug"
    + *Description*: This argument is used to activate debug mode. This is primary used by the developers to figure out why some code is messing up and where in the script. It is by default `False` and off. Simply calling the argument changes it to `True`.
+ **Remove Intermediate IntAct Data JSON**
    + "-r", "--removejson"
    + *Description*: This argument is used to turn on or off the cleanup() process in the script which removes the chunky IntAct JSON, as normally the JSON is to large for any convient use on the user's end after it has been used by the program. It is **by default** `True` and **turned on.** Simply calling the argument changes it to `False`.
+ **Edge List Header Toggle**
    + "-e", "--header"
    + *Description*: This argument is used as a way to control whether you wish for the final output file to have headers for the edge list or to only have the columns be data. It is **by default** `False` and as such **keeps no headers**. Simply calling the argument changes it to `True`.
+ **No Installation Toggle**
    + "-z", "--no install"
    + *Description*: This argument is used as a way to control whether you wish for the program to install the required packages for you or not. It is **by default** `False` and as such **allows installation**. Simply calling the argument changes it to `True`.

Extra:
*There should be maxium number of ~4000 chemicals that can be utilized as stated by the CTD Batch Query API.*
