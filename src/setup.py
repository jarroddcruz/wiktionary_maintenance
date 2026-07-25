'''
Houses functions for setting up:
    user-agent credentials,
    what Wiktionary edition to edit, 
    and what language to work on, 

ensuring API connection is successful
'''

import src.cache as cache
import os
from src.api_requests import get_category_members

api_url_prefix = "https://"
api_url_suffix = ".wiktionary.org/w/api.php"

# Allows user to input new credentials for user-agent before caching it
def set_credentials():
    while True:
        project = input("Enter name of project: ")
        version = input("Enter version number: ")
        wikt_username = input("Enter Wiktionary username: ")
        email = input("Enter email for contact: ")

        user_agent = f'{project}/{version} (User:{wikt_username}; {email})'
        print(f'Your credentials are: {user_agent}')
        response = input('Does this look correct? (Y/n): ')

        if response != "Y":
            continue
        else:
            break

    contents = {
        'project': project,
        'version': version,
        'wikt_username': wikt_username,
        'email': email
    }

    cache.write_json("last_credentials", contents)

    return user_agent

# Attempts to get last used user credentials to speed things up
def get_credentials():
    try:
        credentials = {
        "project": "",
        "version": "",
        "wikt_username": "",
        "email": "",
        }  

        contents = cache.read_json("last_credentials")

        credentials["project"] = contents["project"]
        credentials["version"] = contents["version"]
        credentials["wikt_username"] = contents["wikt_username"]
        credentials["email"] = contents["email"]

        return credentials
    
    except FileNotFoundError:
        return {}

# Establishes which edition of Wiktionary is being worked on; relevant for selecting correct API endpoint
def set_wikt_edition():
    while True:
        valid_eds = ["en"] # Should this be placed in a separate file storing all constants?
        edition = input(f'\nList of supported Wiktionary editions — {valid_eds}\nSelect a Wiktionary edition to work with from the list above: ')
        if edition in valid_eds:
            return edition
        else:
            print("ERROR: Invalid Wiktionary edition selected.")
            continue

# Establishes which language is being worked on within the chosen Wiktionary edition
def pick_language(edition, api_url, headers):
    language = ""

    while True:
        language = input(f'\nName the language you are working with as it appears on Wiktionary: ')

        all_langs = []
        try:
            all_langs_json = cache.read_json(f'{edition}_langs')
            all_langs.extend(item for item in all_langs_json["langs"])

        except FileNotFoundError:
            all_langs = get_category_members(api_url, "All_languages", headers)
            all_langs_json = {'langs': all_langs}
            cache.write_json(f'{edition}_langs', all_langs_json)

        '''
        TO DO:
        Refactor so that if the language isn't found in cache, it requests category members, caches it once, then checks the cache

        Subsequent checks in the same sessions do not re-cache to reduce API requests
        '''
        
        if f'Category:{language} language' not in all_langs:
            print(f'ERROR: {language} not found on Wiktionary')
            
        else:
            break

    return language

def main():
    # Set up credentials for an informative user-agent header based on credentials from the last session, if possible
    user_agent = ""
    print("Checking if last used credentials are available... ", end="")
    credentials = get_credentials()
    
    if credentials == {}:
        print("\nERROR: Failed to retrieve last used credentials. Please input new credentials.")
        user_agent = set_credentials()

    else:
        print("Successful!")
        user_agent = f'{credentials["project"]}/{credentials["version"]} (User:{credentials["wikt_username"]}; {credentials["email"]}'
        print(f'Your credentials are: {user_agent}')
        response = input('Does this look correct? (Y/n): ')
        if response != "Y":
            user_agent = set_credentials()
        else:
            pass

    headers = {
        "User-Agent": user_agent
    }

    # Set up correct Wiktionary edition to work with
    edition = set_wikt_edition()
    api_url = api_url_prefix + edition + api_url_suffix
    
    # Set up correct language to work with in the chosen Wiktionary edition
    language = pick_language(edition, api_url, headers)
    '''
    Allow pick_language to retrieve the language code as well, and perhaps pick using the language code to retrieve the language name too
    '''
    print(f'Selection of {language} confirmed.')

    # Set up useful directories 
    os.makedirs(os.path.dirname("input_files/"), exist_ok=True)
    os.makedirs(os.path.dirname("output_files/"), exist_ok=True)

    return [True, api_url, language, headers]