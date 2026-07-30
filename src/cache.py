'''
This contains functions for accessing cached data as json files so that
1. credentials can be saved so that setup is not tedious
2. the tool does not have to make so many API requests for commonly accessed data
'''

import json
import os

# Accesses write to cache file as json
def write_json(filename, dictionary):
    if "cache" not in os.listdir("src/"): # Added to account for a missing cache folder
        os.makedirs("cache",exist_ok=True)
    f = open(f'cache/{filename}.json', "w")
    json.dump(dictionary, f)
    f.close()
    return True


# Reads contents from cache file as json
def read_json(filename):
    f = open(f'cache/{filename}.json', "r")
    ret = json.load(f)
    f.close()
    return ret