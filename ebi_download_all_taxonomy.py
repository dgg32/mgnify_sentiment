import func_ebi_get_attr_and_url
import sys
from threading import Thread
import queue
from threading import Semaphore
import logging
import json
import datetime
import os

writeLock = Semaphore(value = 1)
errorLock = Semaphore(value = 1)
in_queue = queue.Queue()


biome = sys.argv[1]
output_folder = sys.argv[2]
#biome = "root:Environmental:Terrestrial:Soil"

logging.basicConfig(filename='download_ebi_soil_error.log')

def work():
    while True:
        url, dest = in_queue.get()
        
        try:
            #print (url)

            filename = url.split("/")[-2] + ".json"
            url += "/ssu"

            print (url)
            result = func_ebi_get_attr_and_url.get_all_taxonomy(url)
            print (result)

            path = os.path.join(dest, filename)

            output_file = open(path, 'w')
            output_file.write(json.dumps(result))
            output_file.close()



        except Exception as e:
            current_time = datetime.datetime.now() 
            
            errorLock.acquire()
            logging.error(f"{current_time}: {e}")
            errorLock.release()


        in_queue.task_done()


for i in range(10):
    t = Thread(target=work)
    t.daemon = True
    t.start()

url = f"https://www.ebi.ac.uk/metagenomics/api/v1/biomes/{biome}/studies"

#print (url)

results = func_ebi_get_attr_and_url.get_attribute_and_relationships_url(url, ["analyses", "biomes"])

for r in results:
    anaylsis_url = r["analyses"]
    taxonomies = func_ebi_get_attr_and_url.get_attribute_and_relationships_url(anaylsis_url, ["taxonomy"])
    print (taxonomies)
    for t in taxonomies:
        if "taxonomy" in t:
            in_queue.put([t["taxonomy"], output_folder])

in_queue.join()