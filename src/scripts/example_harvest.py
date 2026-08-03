"""
This script fetches examples from existing corpora using a dictionary of headwords and produces a list of words and exact sentence matches found in the corpus.
"""

import pandas as pd
import docx as dx
import os
import sys
from tqdm import tqdm as prog

class Harvester:
	def __init__(self,corpus,dictionary:pd.Series|None):
		self.corpus = corpus
		self.dictionary = dictionary

	def harvest_examples(self):
		import re
		from colorama import Fore
		zero_examples = []
		with open(r"output_files/harvest_examples.md","w",encoding="utf-8") as examples_file:
			for headword in prog(self.dictionary,"Harvesting Examples",unit="headword"):
				examples = 0
				examples_file.write(f"Headword: {headword}\n{'-'*len(headword)}\n")
				for index,pot_example in enumerate(self.corpus):
					if re.search(rf" {headword} ",pot_example):
						examples_file.write(f"{re.sub(f' {headword} ',f' <span style="color:red">{headword}</span> ',pot_example)}\n\n")
						examples += 1
				examples_file.write(f"Examples Found: **{examples}**\n\n")
				if examples == 0:
					zero_examples.append(headword)
			examples_file.close()
		print("Processing Finished!\nharvest_examples.md is in 'output_files'")
		with open(r"output_files/harvest_report.md","w",encoding="utf-8") as report_file:
			report_file.write("# Harvest Report\n")
			report_file.write(f"Headwords with zero examples: {len(zero_examples)} ; or about {len(zero_examples)/len(self.dictionary)*100:.1f}% ({len(zero_examples)}/{len(self.dictionary)}) of the corpus.")
			report_file.close()
		print("Report written to 'output_files' as 'harvest_report.md'")


def ingest_dict(debug_mode:bool):
	import tkinter as tk
	from tkinter import filedialog as fDialog
	root = tk.Tk()
	root.withdraw()
	"""
	Ingests a dictionary in CSV format and outputs a Pandas Series object containing all headwords.
	debug_mode: If `True`, uses hyper specific headers for a particular corpus item. Will not work if said file is not in `input_files`.
	"""
	filepath = fDialog.askopenfilename(
		title="Select a Dictionary CSV",
		filetypes=[("CSV files","*.csv")]
	)
	with open(r"ingestables/Dictionary.csv",encoding="utf-8") as dict_file: # Import Dictionary CSV File
		dictionary = pd.read_csv(dict_file)
		headword_label = "Chatino Word" if debug_mode else input("Enter your column label for headwords: ")
		working_gloss_label = "English" if debug_mode else input("Enter your column label for other language glosses of headwords: ")
		targ_lang_examples_label = "Chatino Example" if debug_mode else input("Enter your column label for target language examples: ")
		working_lang_examples_label = "Spanish Example" if debug_mode else input("Enter your column label for working language examples: ")
		sjq_headwords = dictionary[headword_label]
		eng_headwords = dictionary[working_gloss_label]
		sjq_examples = dictionary[targ_lang_examples_label]
		es_examples = dictionary[working_lang_examples_label]
		dict_file.close()
	print("Dictionary Ingested!")
	return sjq_headwords

def create_harvester():
	"""
	Creates an instance of the `Harvester` class that cleans and holds sentence blocks and headwords.
	"""
	input("Hello, welcome to the Example Harvester.\n Next, you will be asked to select a valid CSV file that contains your dictionary data.\nPress Enter to Continue...")
	import re
	sjq = ingest_dict(True)
	with open(r"ingestables\corpora\Plaintext Versions\chatino_glosses.txt",encoding="utf-8") as sjq_corpus:
		sentence_blocks = sjq_corpus.read().split("\n\n")
		for index,s_block in enumerate(sentence_blocks):
			sentence_blocks[index] = re.sub(r"\n"," ",s_block)
		#print(sentence_blocks)
	print("Harvester Created!")
	return Harvester(sentence_blocks,sjq)
	
	

harvester = create_harvester()

harvester.harvest_examples()