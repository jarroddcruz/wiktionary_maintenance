import src.setup as setup
import sys
import importlib

def menu(api_url, language, headers):

    '''
    List of scripts that will show up on the main menu
    If you want to load a new script, add a new entry to this scripts dictionary in this format:

    '[INPUT]'   :   {'description':   "[BRIEF DESCRIPTION]",
                     'script_name':   "src.scripts.[SCRIPT_FILENAME (no .py)]"},
    '''
    scripts = {
        'D'     : {'description':   "Compare headwords on spreadsheet vs. Wiktionary",
                   'script_name':   "src.scripts.compare_headwords"},

        'G'     : {'description':   "Get contents of entries in a certain Wiktionary category",
                   'script_name':   "src.scripts.get_entry_wikitext"},
                   
        'H'     : {'description':   "Harvest examples from your corpora based on a dictionary of headwords",
					'script_name':   "src.scripts.example_harvest.example_harvest"},
        'Q'     : {'description':   "Quit",
                   'script_name':   False},
    }

    # Variable to hold anything returned by a script, if needed
    script_ret = ''

    # Formats and displays menu
    while True:
        print('\n=========Wiktionary Maintenance Tool=========\n')
        for key, value in scripts.items():
            print(f'{key} — {value["description"]}')

        try:
            response = input('\nSelect an option: ').upper()
            mod_name = scripts[response]['script_name']

            # Q for Quit
            if mod_name == False:
                break
            else:
                # Imports a script only when chosen
                mod_obj = importlib.import_module(mod_name)

                script_ret = mod_obj.run(api_url, language, headers)

        except KeyError:
            print(f'ERROR: "{response}" is invalid. Select a valid option.')
    

def main():
    # Set up and verify API connection & language edition, user-agent header, and language to be worked on
    setup_ret = setup.main()
    if setup_ret[0] == False:
        sys.exit()

    api_url, language, headers = setup_ret[1], setup_ret[2], setup_ret[3]

    menu(api_url, language, headers)

main()