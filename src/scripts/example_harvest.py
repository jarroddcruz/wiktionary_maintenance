"""
This script fetches examples from existing corpora using a dictionary of headwords and produces a list of words and exact sentence matches found in the corpus.
"""

import pandas as pd
import docx as dx
import os
import sys
from tqdm import tqdm as prog
import tkinter as tk
from tkinter import filedialog as fDialog
root = tk.Tk()
root.withdraw()

def ct(platform=sys.platform):
	"""
	Utility function to clear the terminal window.
	"""
	import subprocess as subp
	subp.run("cls",shell=True) if platform == "win32" else subp.run("clear",shell=True)

def select_list_item(items:list,query:str,*,no_newlines:bool=False,emit_index:bool=False):
	"""
	Utility function to return an item selection from an iterable passed to it.
	"""
	ct()
	print(query)
	for num,item in zip(range(1,len(items)+1),items):
		print(f"{num}. {item}",end=" | ") if no_newlines else print(f"{num}. {item}")
	selection = int(input("\n\nChoice (as #): "))
	return items[selection-1] if emit_index == False else (items[selection-1],selection-1)

class Harvester:
	def __init__(self,corpus,dictionary:pd.Series|None):
		self.corpus = corpus
		self.dictionary = dictionary

	def harvest_examples(self):
		import re
		from colorama import Fore
		zero_examples = []
		save_docname = fDialog.asksaveasfilename(initialdir="output_files")
		with open(f"{save_docname}.md","w",encoding="utf-8") as examples_file, open(f"{save_docname}.csv","w", encoding="utf-8") as csv_examples_file:
			csv_examples_file.write("Headword\n")
			for headword in prog(self.dictionary,"Harvesting Examples",unit=" headwords"):
				examples = 0
				examples_file.write(f"Headword: {headword}\n{'-'*len(headword)}\n")
				csv_examples_file.write(f"{headword},")
				for index,pot_example in enumerate(self.corpus):
					if re.search(rf" {headword} ",pot_example):
						examples_file.write(f"{re.sub(f' {headword} ',f' <span style="color:red">{headword}</span> ',pot_example)}\n\n")
						csv_examples_file.write(f"{pot_example},")
						examples += 1
				examples_file.write(f"Examples Found: **{examples}**\n\n")
				if examples == 0:
					zero_examples.append(headword)
				csv_examples_file.write("\n")
			csv_examples_file.close()
			examples_file.close()
		print(f"Processing Finished!\n{save_docname}.md and {save_docname}.csv are saved to your selected folder")
		with open(os.path.join("output_files","harvest_report.md"),"w",encoding="utf-8") as report_file:
			report_file.write("# Harvest Report\n")
			report_file.write(f"Headwords with zero examples: {len(zero_examples)} ; or about {len(zero_examples)/len(self.dictionary)*100:.1f}% ({len(zero_examples)}/{len(self.dictionary)}) of the corpus.")
			report_file.close()
		print("Report written to 'output_files' as 'harvest_report.md'")


def ingest_dict(debug_mode:bool=False):
	"""
	Ingests a dictionary in CSV format and outputs a Pandas Series object containing all headwords.
	debug_mode: If `True`, uses hyper specific headers for a particular corpus item. Will not work if said file is not in `input_files`.
	"""
	ct()
	input("Next, you will be asked to select a valid .csv file that contains your dictionary of headwords.\nPress Enter to Continue...")
	filepath = fDialog.askopenfilename(
		title="Select a Dictionary CSV",
		filetypes=[("CSV files","*.csv")]
	)
	with open(filepath,encoding="utf-8") as dict_file: # Import Dictionary CSV File
		dictionary = pd.read_csv(dict_file)
		dict_columns = dictionary.columns.to_list()
		headword_label = "Chatino Word" if debug_mode else select_list_item(dict_columns,"Select your column label for target language headwords:\n")
		#working_gloss_label = "English" if debug_mode else select_list_item(dict_columns,"Enter your column label for other language glosses of headwords:\n")
		#targ_lang_examples_label = "Chatino Example" if debug_mode else select_list_item(dict_columns,"Enter your column label for target language examples:\n")
		#working_lang_examples_label = "Spanish Example" if debug_mode else select_list_item(dict_columns,"Enter your column label for working language examples:\n")
		sjq_headwords = dictionary[headword_label]
		#eng_headwords = dictionary[working_gloss_label]
		#sjq_examples = dictionary[targ_lang_examples_label]
		#es_examples = dictionary[working_lang_examples_label]
		dict_file.close()
	print("Dictionary Ingested!")
	return sjq_headwords

def create_harvester():
	"""
	Creates an instance of the `Harvester` class that cleans and holds sentence blocks and headwords.
	"""
	ct()
	input("Hello, welcome to the Example Harvester.\nNext, you will be asked to select a valid .txt file that contains your corpus's examples.\nPress Enter to Continue...")
	import re
	filepath = fDialog.askopenfilename(
			title="Select a File",
			filetypes=[("Text files","*.txt")])
	sjq = ingest_dict()
	with open(filepath,encoding="utf-8") as sjq_corpus:
		sentence_blocks = sjq_corpus.read().split("\n\n")
		for index,s_block in enumerate(sentence_blocks):
			sentence_blocks[index] = re.sub(r"\n"," ",s_block)
		#print(sentence_blocks)
	print("Harvester Created!")
	return Harvester(sentence_blocks,sjq)
	
def run(api_url, language, headers): 
	harvester = create_harvester()
	harvester.harvest_examples()