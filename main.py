import src.setup as setup
import src.diffchecks as diff
import src.entry_contents as entry_contents
import os
import sys

def main():
    # Set up and verify API connection & language edition, user-agent header, and language to be worked on
    setup_ret = setup.main()
    if setup_ret[0] == False:
        sys.exit()
    api_url, language, headers = setup_ret[1], setup_ret[2], setup_ret[3]

    # Set up useful directories 
    os.makedirs(os.path.dirname("output_files/"), exist_ok=True)
    os.makedirs(os.path.dirname("spreadsheets/"), exist_ok=True)

    # Menu
    while True:
        '''
        TO DO: Update menu'''
        menu = ('\n=========Wiktionary Maintenance Tool=========\n'
                'What would you like to do?\n'
                '* D - Diffcheck headwords\n'
                '* G - Get entry contents\n'
                '* Q - Quit\n'

                )
            
        print(menu)
        response = input("Type here: ")

        if response == "D":
            ret = diff.compare_headwords(api_url, language, headers)
            print(f'Matches with wikt: {ret["in_wikt"]}')
            print(f'Missing from wikt: {ret["wikt_missing"]}')
            print(f'Additional in wikt: {ret["wikt_additional"]}')

        if response == "G":
            ret = entry_contents.get_entry_contents(api_url, language, headers)

            
        if response == "Q":
            break

main()