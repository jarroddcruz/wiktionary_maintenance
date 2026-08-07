"""
This script contains a cleaning function to format data for use in example_harvest.py
"""
import typing as typ
import sys
import os
from tqdm.gui import tqdm as prog
from tkinter import filedialog as fd,messagebox as messbox
from .example_harvest import ct,select_list_item as sli,SJQ_flPRACTTONEtoPRACTONE_MAPS as tonemap

def fix_tones(word:str):
	"""
	This function fixes word strings so that the tone characters are basic letter versions rather than special unicode characters that cannot be manipulated like regular strings.
	"""
	floating =list(tonemap.keys())
	practical = list(tonemap.values())
	mapping = str.maketrans("".join(floating),"".join(practical)) # Makes a translation table out of the two sets of characters
	ret_word = word.translate(mapping) # Translates the word
	return ret_word # Returns the translated word


def clean(exp_mode:bool=False):
	"""
	This function attempts to clean files for use with the example finder. It expects sentences each on their own line. 
	Currently cannot handle super complex IGT.
	exp_mode: If `True`, enables experimental mode, which uses regex to try and clean really complex files.
	"""
	import regex as re
	ct()
	input("Welcome to the Cleaner\nPress enter to select the folder containing the files you wish to clean.\nThis is where the cleaned versions will be output.")
	cleaning_dir = fd.askdirectory(title="Select Cleaning Directory",initialdir="input_files") # User selects location for cleaned_files folder.
	files_to_clean = fd.askopenfilenames(title="Select Files to Clean",filetypes=[("Text files","*.txt")],initialdir=cleaning_dir) # User selects files they wish to clean.
	while files_to_clean != "":
		if files_to_clean == '': # If they select no files, delete extra variables and continue without cleaning.
			del cleaning_dir
			del files_to_clean
			return
		conf = messbox.askquestion("Confirmation","Do you want to process the following files?",detail="\n".join([(re.search(r"([^\\]*\w*\.txt)$",filepath).group(1)) for filepath in files_to_clean]))
		if conf:
			cleaned_files_dir = os.path.join(cleaning_dir,"cleaned_files")
			os.makedirs(cleaned_files_dir,exist_ok=True)
			
			for filename in prog(files_to_clean,"Cleaning Files",colour="green"):
				ct()

				# Open two files, one that reads the original corpus .txt, and one to write to; the new, cleaned corpus .txt.
				with open(filename,"r",encoding="utf-8") as readFile, open(os.path.join(cleaned_files_dir,f"cleaned_{os.path.basename(filename)}"),"w",encoding="utf-8") as writeFile:
					fileStr = readFile.read()
					if exp_mode: # EXPERIMENTAL
						fileStr = re.sub(r"\n{2,}","\n",fileStr)
						fileStr = re.sub(r"\t{2,}|\h\t{2,}","\t",fileStr)
						fileStr = re.sub(r"\t{2,}|\h{1,}\t{1,}|\t{1,}\h{1,}","\t",fileStr)
						fileStr = re.sub(r"\h{1,}$|\t{1,}$|^\t{1,}","",fileStr)

						numLines_in_igt = int(input("How many lines does your IGT have?\nThis includes free translation lines.\n# of Lines: "))
						all_lines = fileStr.splitlines(keepends=True)
						linesample = fileStr.splitlines(keepends=True)[:numLines_in_igt]
						baseline_line = sli(linesample,"Which line from this contains the original text?",emit_index=True)
					else: # DEFAULT
						sents = fileStr.splitlines() # Split into sentences
						for sent in sents:
							words = [fix_tones(wrd.strip(" .")) for wrd in sent.split()] # Split sentences into words and fix the tone characters.
							writeFile.write("\n".join(words)) # Write the block of words
							writeFile.write("\n\n") # separate for the next sentence
						readFile.close()
						writeFile.close()
			return
