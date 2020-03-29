import tkinter as tk
import os
import fnmatch as fn

class CovidGUI():
	def __init__(self, root):
		self.root = root
		self.data_dir = "daily-stats/"
		self.root.geometry("800x600")
		self.root.title("COVID-19 Stats by jiricodes")
		self.check_data()
	
	def check_data(self):
		if os.path.exists(self.data_dir):
			print("Checking Available Data")
			for file in os.listdir(self.data_dir):
				if fn.fnmatch(file, '*.json'):
					print(file)
		else:
			print("Requires daily-stats folder")