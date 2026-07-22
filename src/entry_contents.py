'''
Functions for accessing page contents from Wiktionary as wikitext
'''

import csv
import re
import sys

from src.api_requests import get_category_members, get_pages_as_json

def get_entry_contents(api_url, language, headers):
    '''
    TO DO: Allow this to function without having to do get_category_members; this is just to prove it works 
    '''

    response = input(f'What category would you like to get entry contents of (ex. \"{language} proper nouns\")?\nTIP: Simply type \"all\" to compare with \"{language} lemmas\".\n')
    # A shorthand since searching for lemmas will be frequent
    if response == "all":
        response = f'{language} lemmas' 
        '''TO DO: Figure out if I can request multiple categories so I can request non-lemma forms too.'''

    wikt_headwords = get_category_members(api_url, response, headers)

    print(f"Found {len(wikt_headwords)} entries")

    # Fetch definitions
    pages = get_pages_as_json(api_url, language, wikt_headwords, headers)

    # csv output
    filename = input("Provide a filename for the output: ")
    filename = "output_files/" + filename
    if not filename.endswith(".csv"):
        filename += ".csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Definitions"])
        writer.writerows(pages.items())
        f.close()

    print(f"\nSaved {len(wikt_headwords)} entries to {filename}")