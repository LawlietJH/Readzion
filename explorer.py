
# Python 2 y 3
# explorer.py
# LawlietJH
# v1.2.3

from tkinter import filedialog
try: from Tkinter import Tk
except: from tkinter import Tk
import os


root = Tk()
root.withdraw()
root.wm_attributes('-topmost', True)

class Explorer():
	
	def use():
		print('''\n\n	Ejemplo de Uso:

		from explorer import Explorer as ex

		file_name = ex.getFileName()
		print(file_name)

		folder_path = ex.getFolderName()
		print(folder_path)
		
		file_name_save = ex.getFileNameSave()
		print(file_name_save)

		ex.use()''')
	
	def getFileName(title='', file_types=[ 
				['Archivos de Texto','.txt'], ['Todos los Archivos','.*']
			], init_dir=os.getcwd()):
		
		f_name = filedialog.askopenfile(title = title,
										initialdir = init_dir,
										filetypes = file_types)
		if not f_name == None:
			return f_name.name
	
	
	def getFolderName(title='', init_dir=os.getcwd()):
		
		d_path = filedialog.askdirectory(title = title, initialdir = init_dir)
		return d_path
	
	
	def getFileNameSave(file_types=[
					['Archivos de Texto','.txt'], ['Todos los Archivos','.*']
				], title='', init_dir=os.getcwd()):
		
		f_name = filedialog.asksaveasfilename(title = title,
											  initialdir = init_dir,
											  filetypes = file_types)
		if not f_name == None:
			return f_name

