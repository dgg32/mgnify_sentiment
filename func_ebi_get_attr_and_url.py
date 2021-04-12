import requests
import json
from six.moves import urllib
import os





## keyword wa, taxonomy-lsu toka, taxonomy toka

def get_attribute_and_relationships_url(url, keywords):

    content = json.loads(requests.get(url).content)

    
    results = []
    

    while True:

        #print ("page " + str(page))

        data = content["data"]

        if isinstance(data, list):

            for odata in data:
                #print (sample)

                #print (sample)

                temp = {}

                if "attributes" in odata:
                    temp["attributes"] = odata["attributes"]

                if "relationships" in odata:
                    
                    for keyword in keywords:
                        if keyword in odata["relationships"] and "links" in odata["relationships"][keyword] and "related" in odata["relationships"][keyword]["links"]:
                            keyword_url = odata["relationships"][keyword]["links"]["related"]

                            temp[keyword] = keyword_url
                
                results.append(temp)
        else:
            temp = {}

            if "attributes" in data:
                temp["attributes"] = data["attributes"]

            if "relationships" in data:
                
                for keyword in keywords:
                    if keyword in data["relationships"] and "links" in data["relationships"][keyword] and "related" in data["relationships"][keyword]["links"]:
                        keyword_url = data["relationships"][keyword]["links"]["related"]

                        temp[keyword] = keyword_url
            
            results.append(temp)
            #break
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break


    return results


def get_all_interpro (url):
    
    page = requests.get(url).content

    #print (url)
    #print (page)

    content = json.loads(page)

    results = []
    while True:

        data = content["data"]

        for odata in data:

            temp = {}

            if "attributes" in odata:
                att = odata["attributes"]

                if "accession" in att and "count" in att:
                    temp[att["accession"]] = {"count": att["count"], "description": ""}

                    if "description" in att:
                        temp[att["accession"]]["description"] = att["description"] 

            results.append(temp)

        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:

            next_url = content["links"]["next"]

            print (next_url)
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return results


###it work for both go-terms and go-slim
def get_all_go (url):
    content = json.loads(requests.get(url).content)

    results = []
    while True:

        data = content["data"]

        for odata in data:

            temp = {}

            if "attributes" in odata:
                att = odata["attributes"]

                if "accession" in att and "count" in att:
                    temp[att["accession"]] = {"count": att["count"], "description": "", "lineage": ""}

                    if "description" in att:
                        temp[att["accession"]]["description"] = att["description"]

                    if "lineage" in att:
                        temp[att["accession"]]["lineage"] = att["lineage"] 

            results.append(temp)

        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:

            next_url = content["links"]["next"]

            #print (next_url)
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return results


def get_all_taxonomy (url):

    content = json.loads(requests.get(url).content)

    results = []
    while True:

        data = content["data"]

        for odata in data:

            temp = {}

            if "attributes" in odata:
                att = odata["attributes"]

                if "name" in att and "count" in att:
                    temp[att["name"]] = {"count": att["count"], "rank": "", "lineage": ""}

                    if "rank" in att:
                        temp[att["name"]]["rank"] = att["rank"]

                    if "lineage" in att:
                        temp[att["name"]]["lineage"] = att["lineage"] 

            results.append(temp)

        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:

            next_url = content["links"]["next"]

            #print (next_url)
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return results


def get_taxonomy (url, taxon, rank, type, top_domain = "Bacteria"):

    #print (analysis)


    #### attention, epi taxonomy is not accumulative, "Bacteria" is only unclassified Bacteria
    content = json.loads(requests.get(url).content)

    bacteria_rank = "super kingdom"
    #top_domain = "Bacteria"

    if type == "taxonomy-ssu":
        bacteria_rank = "super kingdom"
    elif type == "taxonomy":
        bacteria_rank = "kingdom"

    target_count = 0
    bacteria_count = 0

    while True:

        data = content["data"]

        for odata in data:

            temp = {}

            if "attributes" in odata:
                att = odata["attributes"]

                if "hierarchy" in att and rank in att["hierarchy"] and att["hierarchy"][rank] == taxon and "count" in att:
                    target_count += int(att["count"])

                if "hierarchy" in att and bacteria_rank in att["hierarchy"] and att["hierarchy"][bacteria_rank] == top_domain and "count" in att:
                    bacteria_count += int(att["count"])
            #break
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return [target_count, bacteria_count]


def get_biome(biome_url):
    content = json.loads(requests.get(biome_url).content)

    biomes = []

    while True:

        data = content["data"]

        if isinstance(data, list):

            for odata in data:

                if "id" in odata and odata["id"] not in biomes:
                    biomes.append(odata["id"])
        else:
            if "id" in data and data["id"] not in biomes:
                biomes.append(data["id"])


        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break
        


    return (biomes)


def get_geocoordinates(geocoordinates_url):

    content = json.loads(requests.get(geocoordinates_url).content)

    geocoordinates = []

    while True:

        data = content["data"]

        if isinstance(data, list):
            for odata in data:

                longitude = 0
                latitude = 0

                if "attributes" in odata:
                    att = odata["attributes"]

                    if "longitude" in att:
                        longitude = att["longitude"]

                    if "latitude" in att:
                        latitude = att["latitude"]
                
                if {"latitude": latitude, "longitude": longitude} not in geocoordinates:
                    geocoordinates.append({"latitude": latitude, "longitude": longitude})
        else:
            longitude = 0
            latitude = 0

            if "attributes" in data:
                att = data["attributes"]

                if "longitude" in att:
                    longitude = att["longitude"]

                if "latitude" in att:
                    latitude = att["latitude"]
            
            if {"latitude": latitude, "longitude": longitude} not in geocoordinates:
                geocoordinates.append({"latitude": latitude, "longitude": longitude})
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return (geocoordinates)

def get_sample_metadata (sample_url):
    contents = get_attribute_and_relationships_url(sample_url, ["biome"])

    results = []

    for content in contents:
        temp = {}

        if "latitude" in content["attributes"]:
            temp["latitude"] = content["attributes"]["latitude"]

        if "longitude" in content["attributes"]:
            temp["longitude"] = content["attributes"]["longitude"]

        if "sample-desc" in content["attributes"]:
            temp["sample-desc"] = content["attributes"]["sample-desc"]

        if "accession" in content["attributes"]:
            temp["accession"] = content["attributes"]["accession"]

        temp["biome"] = content["biome"].split("/")[-1].replace("?format=json", "").replace("%20", " ")

        results.append(temp)

    return results



def get_16s_fasta (url, dest):

    content = json.loads(requests.get(url).content)

    while True:

        data = content["data"]

        for odata in data:

            if "attributes" in odata:
                att = odata["attributes"]

                format = "tsv"

                if "file-format" in att and "extension" in att["file-format"]:
                    format = att["file-format"]["extension"]

                if "description" in att and "description" in att["description"]:

                    if (att["description"]["description"] == "All reads encoding SSU rRNA" or att["description"]["description"] == "All reads encoding 16S rRNA") and format == "fasta":

                        if "links" in odata and "self" in odata["links"]:
                            fasta_url = odata["links"]["self"]

                            filename = fasta_url.split("/")[-1].replace("?format=json", "")
                            
                            #print (fasta_url)


                            path = os.path.join(dest, filename)

                            if not os.path.exists(path):

                                ##### there is some link is dead, urlretrieve will return HTTPError, which cannot by serialised. Adding exception handler can deal with the problem
                                try:
                                    urllib.request.urlretrieve(fasta_url, path)
                                except:
                                    pass
                
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

def get_SSU_MAPSeq(url, dest):
    content = json.loads(requests.get(url).content)

    while True:

        data = content["data"]

        for odata in data:

            if "attributes" in odata:
                att = odata["attributes"]

                target_format = "tsv"
                format = "tsv"

                if "file-format" in att and "extension" in att["file-format"]:
                    format = att["file-format"]["extension"]

                if "description" in att and "description" in att["description"]:

                    if att["description"]["description"] == "MAPSeq output file for SSU" and format == target_format:

                        if "links" in odata and "self" in odata["links"]:
                            tsv_url = odata["links"]["self"]

                            filename = tsv_url.split("/")[-1].replace("?format=json", "")
                            
                            #print (fasta_url)


                            path = os.path.join(dest, filename)

                            if not os.path.exists(path):

                                ##### there is some link is dead, urlretrieve will return HTTPError, which cannot by serialised. Adding exception handler can deal with the problem
                                try:
                                    urllib.request.urlretrieve(tsv_url, path)
                                except:
                                    pass
                
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break


def get_sequence(url, dest, identify_string):
    content = json.loads(requests.get(url).content)

    downloaded_files = []

    while True:

        data = content["data"]

        for odata in data:

            if "attributes" in odata:
                att = odata["attributes"]

                target_format = "fasta"
                format = "fasta"

                if "file-format" in att and "extension" in att["file-format"]:
                    format = att["file-format"]["extension"]

                if "description" in att and "description" in att["description"]:

                    if att["description"]["description"] == identify_string and format == target_format:

                        if "links" in odata and "self" in odata["links"]:
                            tsv_url = odata["links"]["self"]

                            filename = tsv_url.split("/")[-1].replace("?format=json", "")
                            
                            #print (fasta_url)


                            path = os.path.join(dest, filename)

                            if not os.path.exists(path):

                                ##### there is some link is dead, urlretrieve will return HTTPError, which cannot by serialised. Adding exception handler can deal with the problem
                                try:
                                    urllib.request.urlretrieve(tsv_url, path)

                                    downloaded_files.append(path)
                                except:
                                    pass
                
        
        if "links" in content and "next" in content["links"] and content["links"]["next"] != None:
            next_url = content["links"]["next"]
            content = json.loads(requests.get(next_url).content)
            
            #break
        else:
            break

    return downloaded_files

if __name__ == '__main__':

    import json

    #result = get_attribute_and_relationships_url("https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Freshwater:Lentic:Sediment/studies", ["analyses", "biomes"])

    #result = get_biome("https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00002103/biomes")
    #result = get_taxonomy("https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00363146/taxonomy/ssu", "Planctomycetes", "phylum", "taxonomy-ssu")
    #print (len(result_url))

    #result = get_geocoordinates("https://www.ebi.ac.uk/metagenomics/api/v1/studies/MGYS00004531/geocoordinates")
    #print (json.dumps(result, indent=4))

    #get_16s_fasta("https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00362651/downloads", "/home/sih13/Downloads/tmp")


    #https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00366145
    # prefix = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/"
    
    # analyses_url = prefix + "MGYA00366145"
    # analyses = get_attribute_and_relationships_url(analyses_url, ["downloads"])

    # for analysis in analyses:
    #     download_url = analysis["downloads"]

    #     get_SSU_MAPSeq(download_url, "/home/sih13/Downloads/tmp")

    #result = get_all_interpro("https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00373161/interpro-identifiers?format=json&page=1")

    #result = get_all_go("https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00373161/interpro-identifiers?format=json&page=1")

    #print (result)

    #download_url = "https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00372711/downloads?format=json"
    #dest = "/home/sih13/Downloads/tmp"
    #get_sequence(download_url, dest, "Processed nucleotide reads")

    print (get_all_taxonomy("https://www.ebi.ac.uk/metagenomics/api/v1/analyses/MGYA00555783/taxonomy/ssu"))