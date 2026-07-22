'''
This contains functions carrying out the basic API requests.
'''

import requests
import time
import sys
import re

'''
TO DO:
Have each API request check cache for a recent request. If there isn't a recent request, request, then cache it.

Maybe have a cache function for reading from en_langs.json specifically?
'''





'''
TO DO: Function that can be called to perform the API request and return the results and/or relevant status codes / http error codes
'''
# def request_check():





'''
TO DO: be able to recurse through subcategories to retrieve pages
https://stackoverflow.com/questions/19223431/get-all-category-members-and-go-over-subcategories-in-mediawiki-api

Possibly relatedly, be able to get members of multiple named categories in one request.
'''
# Retrieves list of pages that directly fall under a single category
def get_category_members(api_url, category, headers):
    category = category.replace(' ', '_')
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f'Category:{category}',
        "cmlimit": "max",
        "format": "json"
    }

    members = []
    while True:
        r = requests.get(api_url, params=params, headers=headers)
        data = r.json()

        members.extend(item["title"] for item in data["query"]["categorymembers"])

        if "continue" not in data:
            break

        params["cmcontinue"] = data["continue"]["cmcontinue"]

    return members

# Retrieve JSON of some named pages
def get_pages_as_json(api_url, language, pages, headers):
    params = {
    "action": "query",
    "prop": "revisions",
    "titles": '|'.join(pages),
    "rvprop": "content",
    "rvslots": "main",
    "format": "json"
    }

    page_contents = {}

    while True:
        r = requests.get(api_url, params=params, headers=headers) 
        data = r.json()
        pages_from_json = data.get("query", {}).get("pages", {})

        for i, id in enumerate(pages_from_json):
            word = pages_from_json.get(id, {}).get("title", {})
            print(f"[{i+1}/{len(pages)}] {word}")

            rev = pages_from_json.get(id, {}).get("revisions", {})
            if not rev:
                sys.exit()
            
            text = rev[0]["slots"]["main"]["*"]

            print(text)

            in_lang = False
            
            entries = []

            for line in text.splitlines():
                if in_lang == True and re.search("==[^=]", line[:3]):
                    in_lang = False
                    break

                if line.startswith(f'=={language}=='):
                    in_lang = True

                if in_lang == True:
                    entries.append(line.strip())

            if entries:
                page_contents[word] = "\n".join(entries)
        
        if "continue" not in data:
            break

        params["cmcontinue"] = data["continue"]["cmcontinue"]
        
    return page_contents
