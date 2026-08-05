
# Introduction
This is a basic command line tool designed for endangered language speakers to upload and maintain entries for eventual incorporation into Wiktionary. We are working with a speaker of San Juan Quiahije Chatino.

This work is being conducted at the Machine Learning for Endangered Language Documentation (MELD) Lab @ University of Florida. 

# Contents
* main.py: The script to run when starting up the tool; allows you to set up credentials for the API and then work with data
* src/: directory containing scripts for frequent operations and for more specific tasks
    * api_requests.py: functions for basic operations with the MediaWiki Action API
    * cache.py: Functions for accessing cached information, such as last used user-agent credentials, entries in language categories, to reduce API load
    * setup.py: Sets up user-agent credentials, what Wiktionary edition to edit, and what language to work on, ensuring API connection is successful
    * scripts/: directory containing scripts for specific tasks; subject to the most development
        * get_entry_wikitext.py: Retrieves wikitext of entries in a certain Wiktionary category
        * compare_headwords.py: Compares entries found in a specified spreadsheet and a Wiktionary category
        <!--* batch_operations.py:-->
        * harvest_corpora.py: Harvests example sentences from a dictionary of headwords and a provided corpus.

# How to contribute
If you would like to contribute to this project, pick an active Issue, make your own branch to implement your solution, and submit a pull request. Feel free to write under the issue or contact me, @jarroddcruz, for any clarification. Here are some things to consider:
* src/scripts contains functions designed for very specific tasks, like comparing headwords between a dictionary spreadsheet and Wiktionary. This is where you can start a Python script that you can select from the main menu. On that note, make sure you add an option to select your script by editing the menu() function in main.py.
* src/ is meant to contain a bunch of useful, flexible functions that more than one script may use, such as certain API requests or cache functions. If you plan on creating a very flexible function, consider adding them to the files in src/.
