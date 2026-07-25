
'''
Functions to perform various kinds of diffchecks between Wiktionary and a spreadsheet
'''

import pandas as pd
from src.api_requests import get_category_members

# Compare headwords found in spreadsheet versus those found in a certain category
def run(api_url, language, headers):
    sheet_headwords = []

    while True:
        try:
            # Prompt user to name a valid csv
            filename = input("Enter name of csv to read in input_files folder: ")

            # Read csv file, print numbered list of columns
            data = pd.read_csv("input_files/" + filename + ".csv")
            print(f'Columns found in {filename}.csv: ')
            for i in range(0, len(data.columns.values)):
                print(f'{i}: {data.columns.values[i]}')

            # Ask user to specify by number which column contains headwords
            response = int(input("Select the number corresponding to the headword column.: "))
            headword_col_name = data.columns.values[response] 
            sheet_headwords = data[headword_col_name].dropna()
            break
        except KeyError:
            print(f'ERROR: Invalid number.')
        except FileNotFoundError:
            print(f'ERROR: {filename}.csv not found. Did you put it in the \'input_files\' folder?')

    # Prompt user to name a valid category whose entries they want to compare headwords with
    response = input(f'What category would you like to compare with (ex. \"{language} proper nouns\")?\nTIP: Simply type \"all\" to compare with \"{language} lemmas\".\n')
    # A shorthand since searching for lemmas will be frequent
    if response == "all":
        response = f'{language} lemmas' 
        '''TO DO: Figure out if I can request multiple categories so I can request non-lemma forms too.'''

    wikt_headwords = get_category_members(api_url, response, headers)
    
    # Using sets, identifies what headwords are missing from Wiktionary and are additional in Wiktionary (missing from spreadsheet)
    sheet_set = set(sheet_headwords)
    wikt_set = set(wikt_headwords)

    in_wikt = list(wikt_set.intersection(sheet_set))
    wikt_missing = list(sheet_set - wikt_set)
    wikt_additional = list(wikt_set - sheet_set)

    print(f'Matches with wikt: {in_wikt}\n')
    print(f'Missing from wikt: {wikt_missing}\n')
    print(f'Additional in wikt: {wikt_additional}')
