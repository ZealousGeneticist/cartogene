##############################################
#  Cartogene:                                #
#  Brief description of what this code does  #
#                                            #
# First Write: 02/01/2023                    #
# Last Visit: 05/02/2023                     #
#                                            #
# Luke Mabry <elmabry99@gmail.com>           #
# License: GPL v3.0                          #
##############################################

###USER DEFINED VARIABLES###
#TODO: Move these to command line options:  https://www.knowledgehut.com/blog/programming/sys-argv-python-examples

##Take data of bioactive compounds and ask for what they interact with in homo sapiens
#Retrieve data via CTD's batch Querry Tool, send an HTTP GET request to http://ctdbase.org/tools/batchQuery.go
import requests, sys, json, time, math, os
import pandas as pd
#Define Input and Output Files
infile = 'bioactive.tsv'
outfile1 = 'interactionsCTD.tsv'
outjson = 'faceted_intact_results'
outfile3 = 'faceted_inact_node_network.tsv'
#Define Taxonomy ID
organism=9606

test = False #Omniscience function toggle for single file output
debug = False #Debugging toggle for verbose output

###USER DEFINED FUNCTIONS###

#Define the Program to easily request data from chems and other types of data
def cgixns(infile, outfile1, inputType='chem', actionTypes='ANY', debug=False):
    with open(infile, 'r') as lines:
        inTerms = lines.read()
    #CTD URL Batch Querry with input
    url = 'http://ctdbase.org/tools/batchQuery.go?report=cgixns&format=tsv&inputTerms='
    get = requests.get(url+inTerms+'&'+'inputType='+inputType+'&'+'actionTypes='+actionTypes)
    #Save interaction data in outfile1
    with open(outfile1, 'wb') as b:
        b.write(get.content)
    #Set debug=True if making/editing code
    if debug:
        print(inTerms)
        print(type(get))
        print(f"{get.status_code}: {get.reason}")
        with open(infile, 'rb') as lines:
            print(lines.read())
    return print("Done! Have a great rest of your research, dude! :)")


#Define program to grab all interaction data from IntAct on all genes in CTD Data from cgixns as omniscience
def omniscience(outfile1, outjson, jsonSize=10_000, organism=9606, test=False, debug=False):
    if organism != 9606:
        print('Sorry, currently only humans supported! Come back soon.')
        return
    ###Define function to take outfile1 dataframe and get all interactions between genes
    #Don't need to make them connect yet with chemicals.

    ##Turn outfile1 into a dataframe with pandas
    of1df = pd.read_table(outfile1) #outfile1 dataframe code
    #Select for only human data (assuming human); haa stands for "I'm only Human, After All" (its a meme)
    haa = of1df[of1df["OrganismID"] == 9606]
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
    pm = {"advancedSearch" : True, "intraSpeciesFilter":True, "page": 1, "pageSize": 1, "query":"taxidA:9606 taxidB:9606" + gss}
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
            i += 1
            pm['page'] = i
            outfile2 = outjson + str(i) + '.json'
            print('Saving...')
            with open(outfile2, 'wb') as f:
                for chunk in requests.post(url_facet,params=pm).iter_content(chunk_size=4096):
                    f.write(chunk)
            print('File',i,'saved.\n')
            time.sleep(1)
    #Exiting Messages
    print('Omniscience complete. \n',i,'file(s) have been blessed upon you.')
    print('Please consider using reductionism (the program) on your data so it is inteligible.')
    print('The sciences shall voyage far from our island of ignorance into the midst of black seas of infinity.')


####Make an edge network of source nodes and target nodes (whether chemical or gene)
def reductionism(outfile1, outjson, outfile3, outputHeader=True, organism=9606):
    nodesSource = []
    nodesTarget = []
    print('Oh yeah, reductionism time...\n its all about to be SourceNode or TargetNode up in here... \n Please wait...')
    ###Pull out from content moleculeA & moleculeB
    def nodepull(b,y=[],z=[]):
        for x in json.load(b)['data']['content']:
            y.append(x['moleculeA'])
            z.append(x['moleculeB'])

    #Pull up every outjson file and use for edge table
    with os.scandir() as directory:
        for item in directory:
            if item.name.startswith(outjson) and item.name.endswith('.json') and item.is_file():
                with open(item,'rb') as b:
                    nodepull(b,nodesSource,nodesTarget) #NOTE, should replace later because opening each json is bad
                    print(item.name, 'is done being reduced!')

    ##Put edge list for input chemicals in
    of1df = pd.read_table(outfile1) #outfile1 dataframe code
    #Select for only human data(assuming human); haa stands for "I'm only Human, After All" (its a meme)
    haa = of1df[of1df["OrganismID"] == organism]
    ##select for 4th column values, the CASRN, and save as a list & string
    CasRN = haa[["CasRN","GeneSymbol"]].drop_duplicates(keep='first')
    for x in CasRN.CasRN.to_list():
        nodesSource.append(x)
    for x in CasRN.GeneSymbol.to_list():
        nodesTarget.append(x)

    #Put Node list into node library
    nodes = {'SourceNode':nodesSource,
             'TargetNode':nodesTarget}
    nodedf = pd.DataFrame(nodes)
    ##Sort by row then by column alphanumerically to remove duplicate edges (a-b == b-a)
    nodesort = nodedf.values
    nodesort.sort(axis=1)
    nodedf = pd.DataFrame(nodesort, nodedf.index, nodedf.columns)
    nodedf = nodedf.sort_values(by='SourceNode')
    nodedf = nodedf.drop_duplicates(keep='first')
    #debug
    if debug:
        print(*nodes, sep='\t')
        print(nodedf)

    #Comes down to a 2 column dataframe in outfile3, input for outputHeader
    nodedf.to_csv(outfile3, index=False, sep='\t', header= outputHeader)
    print('Reduced to atoms... or at least: \n',os.stat(outfile3).st_size/1000, 'kB')


### PROGRAM ###
cgixns(infile, outfile1 ,actionTypes='binding')
omniscience(outfile1, outjson)
reductionism(outfile1,outjson,outfile3)
