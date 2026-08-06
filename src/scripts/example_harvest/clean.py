""""
This script contains a cleaning function to format data for use in example_harvest.py
"""
import typing as typ
import sys
import os
from tqdm import tqdm as prog
from tkinter import filedialog as fd,messagebox as messbox
from example_harvest import ct,select_list_item as sli

def clean():
	import regex as re
	ct()
	input("Welcome to the Cleaner\nPress enter to select the folder containing the files you wish to clean.\nThis is where the cleaned versions will be output.")
	cleaning_dir = fd.askdirectory(title="Select Cleaning Directory",initialdir="input_files")
	files_to_clean = fd.askopenfilenames(title="Select Files to Clean",filetypes=[("Text files","*.txt")],initialdir=cleaning_dir)
	conf = messbox.askquestion("Confirmation","Do you want to process the following files?",detail="\n".join([(re.search(r"([^\\]*\w*\.txt)$",filepath).group(1)) for filepath in files_to_clean]))
	if conf:
		cleaned_files_dir = os.path.join(cleaning_dir,"cleaned_files")
		os.makedirs(cleaned_files_dir,exist_ok=True)
		fileNum = 0
		for filename in files_to_clean:
			ct()
			fileNum += 1
			with open(filename,"r",encoding="utf-8") as readFile, open(os.path.join(cleaned_files_dir,f"cleaned_{os.path.basename(filename)}")) as writeFile:
				fileStr = readFile.read()
				fileStr = re.sub(r"\n{2,}","\n",fileStr)
				fileStr = re.sub(r"\t{2,}|\h\t{2,}","\t",fileStr)
				fileStr = re.sub(r"\t{2,}|\h{1,}\t{1,}|\t{1,}\h{1,}","\t",fileStr)
				fileStr = re.sub(r"\h{1,}$|\t{1,}$|^\t{1,}","",fileStr)

				numLines_in_igt = int(input("How many lines does your IGT have?\nThis includes free translation lines.\n# of Lines: "))
				all_lines = fileStr.splitlines(keepends=True)
				linesample = fileStr.splitlines(keepends=True)[:numLines_in_igt]
				baseline_line = sli(linesample,"Which line from this contains the original text?",emit_index=True)
				sys.exit(0)
clean()