"""
This script fetches examples from existing corpora using a dictionary of headwords and produces a list of words and exact sentence matches found in the corpus.
"""
# Imports
import pandas as pd
import docx as dx
import os
import sys
from tqdm import tqdm as prog
import tkinter as tk
from tkinter import filedialog as fDialog, messagebox as messbox
from typing import Iterable

SJQ_flPRACTTONEtoPRACTONE_MAPS = {
	"ᴱ":"E",
	"ᶜ":"C",
	"ᶠ":"F",
	"ꟳ":"F",
	"ᴬ":"A",
	"ᴮ":"B",
	"ᴶ":"J",
	"ᴳ":"G",
	"ᴵ":"I",
	"ᴴ":"H",
	"ᴷ":"K"
}

root = tk.Tk()
root.withdraw()

def ct(platform=sys.platform):
	"""
	Utility function to clear the terminal window.
	"""
	import subprocess as subp
	subp.run("cls",shell=True) if platform == "win32" else subp.run("clear",shell=True)

def select_list_item(items:Iterable,query:str|None=None,*,no_newlines:bool=False,emit_index:bool=False):
	"""
	Utility function to return an item selection from an iterable passed to it.
	"""
	ct()
	print(query)
	for num,item in zip(range(1,len(items)+1),items):
		print(f"{num}. {item}",end=" | ") if no_newlines else print(f"{num}. {item}")
	selection = int(input("\n\nChoice (as #): "))
	return items[selection-1] if emit_index == False else (items[selection-1],selection-1)

class Corpus:
	def __init__(self,filename,corpus,dictionary:pd.Series|None,wl_glosses:pd.Series|None):
		self.filename = filename
		self.corpus = corpus
		self.dictionary = dictionary
		self.wl_glosses = wl_glosses

def harvest_examples(corpora:list[Corpus]):
	"""
	Method to harvest the examples.
	"""
	import re
	from colorama import Fore
	zero_examples = []
	with open(os.path.join("output_files",f"examples.md"),"w",encoding="utf-8") as examples_file, open(os.path.join("output_files",f"examples.csv"),"w", encoding="utf-8") as csv_examples_file:
		dictionary = corpora[0].dictionary
		for headword in prog(dictionary,"Harvesting Examples",unit=" headwords"):
			csv_examples_file.write("Headword\n")
			examples_file.write(f"Headword: {headword}\n{'-'*len(headword)}\n")
			csv_examples_file.write(f"{headword},")
			examples = 0
			corpus_ex_list = []
			for corpus in corpora:
				corpExamples = 0
				for index,pot_example in enumerate(corpus.corpus):
					if re.search(rf" {headword} ",pot_example):
						examples_file.write(f"{re.sub(f' {headword} ',f' <span style="color:red">{headword}</span> ',pot_example)} *({corpus.filename})*\n\n")
						csv_examples_file.write(f"{pot_example},") # Need a way to get citation in CSV
						corpExamples += 1
						examples += 1
				corpus_ex_list.append(corpExamples)
			examples_file.write("\n---\n")
			for corp,numexamples in zip(corpora,corpus_ex_list):
				examples_file.write(f"Examples found in {corp.filename}: **{numexamples}**\n\n")
			examples_file.write(f"Total Examples Found for Headword: **{examples}**\n\n")
			if examples == 0:
				zero_examples.append(headword)
			csv_examples_file.write("\n")
		csv_examples_file.close()
		examples_file.close()
		print(f"Processing Finished!\nexamples_{corpus.filename}.md and examples_{corpus.filename}.csv are saved to your selected folder")
	with open(os.path.join("output_files","harvest_report.md"),"w",encoding="utf-8") as report_file:
		report_file.write("# Harvest Report\n")
		report_file.write(f"Headwords with zero examples: {len(zero_examples)} ; or about {len(zero_examples)/len(dictionary)*100:.1f}% ({len(zero_examples)}/{len(dictionary)}) of the corpus.")
		report_file.close()
	print("Report written to 'output_files' as 'harvest_report.md'")
	if messbox.askyesno("Confirmation","Would you like to perform another harvest?",icon="question"):
		run()
	else:
		ct()


def ingest_dict(debug_mode:bool=False):
	"""
	Ingests a dictionary in CSV format and outputs a Pandas Series object containing all headwords.\n
	debug_mode: If `True`, uses hyper specific headers for a particular corpus ite for testing purposes. Will not work if said file is not in `input_files`.
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
		working_gloss_label = "English" if debug_mode else select_list_item(dict_columns,"Enter your column label for other language glosses of headwords:\n")
		#targ_lang_examples_label = "Chatino Example" if debug_mode else select_list_item(dict_columns,"Enter your column label for target language examples:\n")
		#working_lang_examples_label = "Spanish Example" if debug_mode else select_list_item(dict_columns,"Enter your column label for working language examples:\n")
		sjq_headwords = dictionary[headword_label]
		wl_gloss_headwords = dictionary[working_gloss_label]
		#sjq_examples = dictionary[targ_lang_examples_label]
		#es_examples = dictionary[working_lang_examples_label]
		dict_file.close()
	print("Dictionary Ingested!")
	return sjq_headwords,wl_gloss_headwords

def create_corpus(debug_mode:bool=False) -> list[Corpus]:
	"""
	Creates an instance of the `Harvester` class that cleans and holds sentence blocks and headwords.
	"""
	ct()
	corpora = []
	dictionary = ingest_dict()
	ct()
	input("Hello, welcome to the Example Harvester.\nNext, you will be asked to select a valid .txt file that contains your corpus's examples.\nPress Enter to Continue...")
	import re
	filepaths = fDialog.askopenfilenames(
			title="Select Corpus Files",
			filetypes=[("Text files","*.txt")])
	delim = None
	for fn in filepaths:
		with open(fn,encoding="utf-8") as corpus_file:
			ct()
			if delim == None:
				delim = input("What character is used to separate example sentences?\nFor a single newline, just press enter.\nSpecify newlines using '\\n' and tabs using '\\t'.\nSeparator: ")
			if delim == "":
				delim = "\n"
			sentence_blocks = corpus_file.read().split("\n\n") if debug_mode else corpus_file.read().split(delim)
			for index,s_block in enumerate(sentence_blocks):
				sentence_blocks[index] = re.sub(r"\n"," ",s_block)
			#print(sentence_blocks)
		print("Harvester Created!")
		corpora.append(Corpus(os.path.basename(fn),sentence_blocks,dictionary[0],dictionary[1]))
	return corpora
	
def run(api_url="Y", language="sjq", headers="0"):
	from .clean import clean
	cleanconf = messbox.askyesno("Confirm Cleaning","Would you like to clean corpus texts before running the harvester?")
	if cleanconf:
		ct()
		clean()
		ct()
	corpora_list = create_corpus(True)
	harvest_examples(corpora_list)