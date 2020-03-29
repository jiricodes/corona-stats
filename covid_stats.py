#!/usr/bin/python3
from srcs.covid_gui import CovidGUI
import tkinter as tk

if __name__ == "__main__":
	root = tk.Tk()
	covid = CovidGUI(root)
	root.mainloop()