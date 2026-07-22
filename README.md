
# Introduction
This repository contains work on tools designed for endangered language speakers to upload and maintain dictionary entries on Wiktionary through a master spreadsheet. We are currently working with a speaker of San Juan Quiahije Chatino.

This work is being conducted at the Machine Learning for Endangered Language Documentation (MELD) Lab @ University of Florida. 

# Contents
* main.py: The script to run when starting up the tool; allows you to set up credentials for the API and then work with data
* src/api_requests.py: functions for basic operations with the MediaWiki Action API
* src/cache.py: Functions for accessing cached information, such as last used user-agent credentials, entries in language categories, to reduce API load
* src/diffchecks.py: Functions to perform various kinds of diffchecks
* src/entry_contents.py: Functions for accessing contents of actual pages
* src/setup.py: Sets up user-agent credentials, what Wiktionary edition to edit, and what language to work on, ensuring API connection is successful
* src/batch_operations.py:
* src/harvest_corpora.py:

# To-do:
* Set up API error checks; verification wrapper function that can take in a function as an argument?
https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module 

* https://www.mediawiki.org/wiki/API:Query: "To get data about pages in a certain category, instead of querying list=categorymembers and then querying again with pageids set to all the returned pages, combine the two API calls into one by using generator=categorymembers."