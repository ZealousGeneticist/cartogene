#!/usr/bin/env python3

##############################################
#  Cartogene:                                #
#  Brief description of what this code does  #
#                                            #
# First Write: 02/01/2023                    #
# Last Visit: 10/25/2023                     #
#                                            #
# Luke Mabry <elmabry99@gmail.com>           #
# License: GPL v3.0                          #
##############################################

#Package Installation
import subprocess
import sys
import pkg_resources
def install(package): #Installing process for dependencies
    try:
        # Check if the package is already installed
        pkg_resources.get_distribution(package)
        print(f"{package} is already installed.")
    except pkg_resources.DistributionNotFound:
        # If the package is not installed, install it
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} has been installed.")

install("requests")
import requests, json, time, math, os, argparse
install("pandas")
import pandas as pd
install("str2bool")
from str2bool import str2bool

###USER DEFINED VARIABLES###
##################################
parser = argparse.ArgumentParser()

#infile, Input Chemical List
parser.add_argument("-i", "--input", required=True,
                    help="input file name of chemical list")

#outfile3, Edge List Name
parser.add_argument("-o", "--output", required=False,
                    nargs='?', default="faceted_inact_node_network.tsv", const="faceted_inact_node_network.tsv",
                    help="ouput edge list file name\ndefault='faceted_inact_node_network.tsv'")

#outfile1, CTD Chemical-Gene Interaction Table Name
parser.add_argument("-c", "--ctd", required=False,
                    nargs='?', default="interactionsCTD", const="interactionsCTD",
                    help="CTD chemical-gene interaction file name\ndefault='interactionsCTD'")

#outjson, IntAct (Large) Data File Name
parser.add_argument("-j", "--json", required=False,
                    nargs='?', default="faceted_intact_results", const="faceted_intact_results",
                    help="large orginal IntAct data file name\ndefault='faceted_intact_results'")

#organismID, NCBI Taxonomy Number
parser.add_argument("-g", "--organism", required=False,
                    nargs='?', default=9606, const=9606, 
                    type=int,
                    help="organism NCBI Taxonomy ID number\ndefault=9606")

#test, Omniscience Specific Single-Data-File Tester
parser.add_argument("-t", "--test", required=False,
                    nargs='?', default=False, const=False,
                    help="Used to output only one IntAct JSON to test computing problems\ndefault=False")

#debug
parser.add_argument("-d", "--debug", required=False,
                    nargs='?', default=False, const=False,
                    help="debug mode\ndefault=False")

#removeJSON, Deletes orginal data JSON in cleanup
parser.add_argument("-r", "--removejson", required=False,
                    nargs='?', default=True, const=True,
                    help="cleanup option, set to False to disable\ndefault=True")

#outputHeader, Edge List (outfile3) Header Enable/Disable
parser.add_argument("-e", "--header", required=False,
                    nargs='?', default=False, const=False,
                    help="header option for the final edge list\ncalled '-e' because '-h' is help\ndeafult=False")

args = parser.parse_args()
##################################

#Define Input and Output Files
infile = args.input
outfile3 = args.output
outfile1 = args.ctd
outjson = args.json
organism= args.organism #Define Taxonomy ID
test = str2bool(str(args.test)) #Omniscience function toggle for single file output
debug = str2bool(str(args.debug)) #Debugging toggle for verbose output
removeJSON = str2bool(str(args.removejson)) #Toggle for deleting orginal IntAct JSON file
outputHeader = str2bool(str(args.header)) #Toggle for having headers in the final node library
###USER DEFINED FUNCTIONS###

##Take data of bioactive compounds and ask for what they interact with in homo sapiens
#Retrieve data via CTD's batch Querry Tool, send an HTTP GET request to http://ctdbase.org/tools/batchQuery.go

#Define the program to easily request data from chems and other types of data
def cgixns(infile, outfile1, inputType='chem', actionTypes='ANY', debug=False):
    print('Begining Comparative Toxicogenomics Database (CTD) chemical-gene interaction Batch Query...')
    with open(infile, 'r') as lines:
        inTerms = lines.read()
    #CTD URL Batch Querry with input
    url = 'http://ctdbase.org/tools/batchQuery.go?report=cgixns&format=tsv&inputTerms='
    get = requests.get(url+inTerms+'&'+'inputType='+inputType+'&'+'actionTypes='+actionTypes)
    #Save interaction data in outfile1
    with open(outfile1+'_chemical-protein.tsv', 'wb') as b:
        b.write(get.content)
    #Set debug=True if making/editing code
    if debug:
        print(inTerms)
        print(type(get))
        print(f"{get.status_code}: {get.reason}")
        with open(infile, 'rb') as lines:
            print(lines.read())
    return print("Done with chemical to gene interactions! Have a great rest of your research, dude! :)\n")


#Define program to grab all interaction data from IntAct on all genes in CTD Data from cgixns as omniscience
def omniscience(outfile1, outjson, jsonSize=5_000, organism=9606, test=False, debug=False):
    print('Beginning to grab all interaction data from IntAct on all genes in CTD datatable...')
    ###Define function to take outfile1 dataframe and get all interactions between genes
    #Don't need to make them connect yet with chemicals.

    ##Turn outfile1 into a dataframe with pandas
    of1df = pd.read_table(outfile1+'_chemical-protein.tsv') #outfile1 dataframe code
    #Select for only human data (assuming human); haa stands for "I'm only Human, After All" (its a meme)
    haa = of1df[of1df["OrganismID"] == organism]
    #debug
    if debug:
        print(of1df.head(3))
        print('\n\nNext Table\n\n')
        print(haa.head(3))
    ##select for 5th column values, the genesymbols, and save as a list & string
    genesymbols = haa["GeneSymbol"].drop_duplicates(keep='first')
    gsl = genesymbols.to_list() #genesymbols list variable = gsl
    gss = ''
    for name in gsl:
        if gss == '':
            gss += name
        else:
                gss += ' '+name
    #debug
    if debug:
        print(gss[0:20])
        print(gsl[0:5])

    ##Script to querry for all gene products interactions with the above bioactive compounds
    #Search for interactions with findInteractionWithFacet on IntAct Advanced Search with gss
    url_facet = 'https://www.ebi.ac.uk/intact/ws/interaction/findInteractionWithFacet?'
    #The Parameters
    query = f"taxidA:({organism}) AND taxidB:({organism}) AND geneName:({gss}) AND ((ptypeA:protein) AND (ptypeB:protein))"
    # (((ptypeA:protein) OR (ptypeA:gene)) AND ((ptypeB:protein) OR (ptypeB:gene)))
    pm = {"advancedSearch" : True, "intraSpeciesFilter":True, "page": 0, "pageSize": 1, "query":query}
    post = requests.post(url_facet,params=pm)
    i = 0
    totalele= post.json()['data']['totalElements']
    filenum = math.ceil(totalele / jsonSize)
    #Omniscience feedback#
    print('The number of elements in total:',totalele)
    del totalele
    if ~test:
        print("The number of files shall be:",filenum)
        print('Omniscience prepped. Beginning to write file: \n',(i+1),"of",filenum)
    else:
        print("Since this is a test, there will only be 1 file; normally, the number of files would be:", filenum)
        print('Omniscience prepped.')
    pm['pageSize'] = jsonSize
    del post
    #Estimate Time for each file to download from server
    print('The server will take about',requests.post(url_facet,params=pm).elapsed,'to process each file.\n')

    ###Save interactions data json in folder as outfile2
    #Option to only make 1 file, then fake files to see if the procedure works
    if test:
        if debug:
            print('The # of pages is',filenum)
        while i < filenum:
            if debug:
                print('The # of pages is still',filenum)
            i += 1
            pm['page'] = i
            outfile2 = outjson + str(i) + '.json'
            print('Saving...')
            with open(outfile2, 'w') as f:
                #Making a json for testing with reductionism
                f.write('{"data":{"content":[{"moleculeA":"IMITA","moleculeB":"TION"}]}}')
            print('Saved imitation file-',i,'.\n')
            time.sleep(1)
    else:
        if debug:
            print('The # of pages is',filenum)
        while i < filenum:
            pm['page'] = i
            outfile2 = outjson +'_'+ str(i) + '_PPI.json'
            print('Saving...')
            with open(outfile2, 'wb') as f:
                sam_i_hope_your_right = requests.post(url_facet,params=pm)
                print(sam_i_hope_your_right.status_code)
                for chunk in sam_i_hope_your_right.iter_content(chunk_size=4096):
                    f.write(chunk)
            print('File',i+1,'saved.\n')
            i += 1
            time.sleep(1)
    #Exiting Messages
    print('Omniscience complete. \n',i,'file(s) have been blessed upon you.')
    print('The sciences shall voyage far from our island of ignorance into the midst of black seas of infinity.\n')


####Make an edge network of source nodes and target nodes (whether chemical or gene)
def reductionism(outfile1, outjson, outfile3, outputHeader=True, organism=9606, debug = False):
    print('Oh yeah, reductionism time...\n Please wait...')
    ###Pull out from content moleculeA, moleculeB and add an edgeLabel for PPI
    def nodepull(b,x=[],y=[]):
        for a in json.load(b)['data']['content']:
            x.append(a['moleculeA'])
            y.append(a['moleculeB'])

    #Define function to sort by row then by column alphanumerically to remove duplicate edges (a-b == b-a)
    def dupeRemove(nodeA,nodeB,edgeLabel = ''):
        #Put Node list into a dataframe
        nodes = {'nodeA':nodeA,
                'nodeB':nodeB}
        nodedf = pd.DataFrame(nodes)
        ##Sort by row then by column alphanumerically to remove duplicate edges (a-b == b-a)
        nodesort = nodedf.values
        nodesort.sort(axis=1)
        nodedf = pd.DataFrame(nodesort, nodedf.index, nodedf.columns)
        nodedf = nodedf.sort_values(by='nodeA')
        nodedf = nodedf.drop_duplicates(keep='first')
        #For applying edgeLabel to each set of nodes
        edgeList = [] 
        for x in nodeA:
                edgeList.append(edgeLabel)
        nodedf['edgeType'] = edgeLabel
        return nodedf

    #Pull up every outjson file and use for edge table
    nodesSource = []
    nodesTarget = []
    with os.scandir() as directory:
        for item in directory:
            if item.name.startswith(outjson) and item.name.endswith('_PPI.json') and item.is_file():
                with open(item,'rb') as b:
                    nodepull(b,nodesSource,nodesTarget) #NOTE, should replace later because opening each json is bad
                    print(item.name, 'is done being reduced!')
    
    ##Put edge table for input chemicals in
    node1 = []
    node2 = []
    of1df = pd.read_table(outfile1+'_chemical-protein.tsv') #outfile1 dataframe code
    #Select for only human data(assuming human); haa stands for "I'm only Human, After All" (its a meme)
    haa = of1df[of1df["OrganismID"] == organism]
    ##select for 4th column values, the chemicalName, and save as a list & string
    chemicalName = haa[["ChemicalName","GeneSymbol"]].drop_duplicates(keep='first')
    for a in chemicalName.ChemicalName.to_list():
        node1.append(a)
    for a in chemicalName.GeneSymbol.to_list():
        node2.append(a)

    #Put Node list into node library
    x = dupeRemove(nodesSource,nodesTarget,'PPI')
    y = dupeRemove(node1,node2,'chemical-protein')
    finaldf = pd.concat([x,y],ignore_index=True) #Joining the dataFrames together
    #debug
    if debug:
        print(finaldf)

    #Comes down to a 2 column dataframe in outfile3, input for outputHeader
    finaldf.to_csv(outfile3, index=False, sep='\t', header= outputHeader)
    print('Reduced to atoms... or at least: \n',os.stat(outfile3).st_size/1000, 'kB')

#Function for deleting huge JSON files from omniscience as cleanup
def cleanup(removeJSON):
    if removeJSON:
        with os.scandir() as directory:
            for item in directory:
                if item.name.startswith(outjson) and item.name.endswith('_PPI.json') and item.is_file():
                    os.remove(item)

### PROGRAM ###
print('\n\n\n')
cgixns(infile, outfile1 ,actionTypes='binding')
omniscience(outfile1, outjson)
reductionism(outfile1,outjson,outfile3,outputHeader)
cleanup(removeJSON)