
# Python 3
# Readzion
# v1.0.6

#=======================================================================

#Hide Console
def Hide(xD=True):
	
	import win32console,win32gui
	window = win32console.GetConsoleWindow()
	
	if xD == True:
		win32gui.ShowWindow(window,0)
		return True
	elif xD == False:
		win32gui.ShowWindow(window,1)
		return False

# ~ Hide()

#=======================================================================

# ~ try: import tkinter as tk
# ~ except: import Tkinter as tk

from tkinter import *
# ~ from tkinter.messagebox import *
# ~ from tkinter.filedialog import *
from explorer import Explorer as ex
import base64
import os



exists = lambda file_name: os.path.exists(file_name)
encode = lambda data: base64.urlsafe_b64encode(data)
decode = lambda data: base64.urlsafe_b64decode(data)



class Notepad: 
	
	class StatusBar(Frame):

		def __init__(self, master):
			Frame.__init__(self, master)
			self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
			self.label.pack(fill=X)

		def set(self, format, *args):
			self.label.config(text=format % args)
			self.label.update_idletasks()

		def clear(self):
			self.label.config(text='')
			self.label.update_idletasks()
	
	root = Tk()
	thisWidth = 600
	thisHeight = 400
	# Pagina de colores: https://mycolor.space/?hex=%23002045&sub=1
	thisTextArea = Text(root, bg='#002045', fg='#EBEBFF', bd=2,
		insertbackground='#B5D5F5', selectbackground='#008080')
	thisMenuBar = Menu(root)
	thisFileMenu = Menu(thisMenuBar, tearoff=0)
	
	thisScrollBar = Scrollbar(thisTextArea)      
	_file = None
	rowsNumber = 1
	original_title = 'Sin Nombre'
	title = original_title
	script = 'Readzion'
	unsave = '* (Sin Guardar) - '
	save = ' - '
	
	def __init__(self, **kwargs):
		
		try: self.root.wm_iconbitmap('Notepad.ico')
		except: pass
		
		# Tamano de ventana (Por defecto es de 300x300)
		try:
			self.thisWidth = kwargs['width']
			self.thisHeight = kwargs['height']
		except KeyError: pass
		
		# Titulo de la ventana:
		self.root.title(self.title + self.unsave + self.script)
		
		self.status = self.StatusBar(self.thisTextArea)
		self.status.pack(side=BOTTOM, fill=X)
		self.updateRowsNumber()
		
		# Centrar la ventana:
		screenWidth = self.root.winfo_screenwidth()
		screenHeight = self.root.winfo_screenheight()
		
		# For left-alling
		left = (screenWidth // 2) - (self.thisWidth // 2)
		
		# For right-allign
		top = (screenHeight // 2) - (self.thisHeight //2)
		
		# For top and bottom
		self.root.geometry('{}x{}+{}+{}'.format(self.thisWidth,
										self.thisHeight, left, top))
		
		# To make the textarea auto resizable
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		
		# Add controls (widget)
		self.thisTextArea.grid(sticky = N + E + S + W)
		
		# Barra de Menu:
		self.thisFileMenu.add_command(label='Nuevo', command=self.newFile)
		self.thisFileMenu.add_command(label='Abrir', command=self.openFile)
		self.thisFileMenu.add_command(label='Guardar', command=self.saveFile)
		self.thisFileMenu.add_separator()
		self.thisFileMenu.add_command(label='Cerrar', command=self.exit)
		self.thisMenuBar.add_cascade(label="Archivo", menu=self.thisFileMenu)
		
		self.root.config(menu=self.thisMenuBar)
		self.thisScrollBar.pack(side=RIGHT, fill=Y)
		# Scrollbar will adjust automatically according to the content
		self.thisScrollBar.config(command=self.thisTextArea.yview)
		self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set)
		
		
		self.menu = Menu(self.root, tearoff=0)
		
		self.root.wm_attributes('-topmost', True)
		
		self.root.bind('<Button-3>', self.popup)
		# ~ self.thisTextArea.bind('<Key>', self.changeLineNumber)
		self.thisTextArea.bind('<Control-n>', self.newFile)
		self.thisTextArea.bind('<Control-N>', self.newFile)
		self.thisTextArea.bind('<Control-g>', self.saveFile)
		self.thisTextArea.bind('<Control-G>', self.saveFile)
		self.thisTextArea.bind('<Control-o>', self.openFile)
		self.thisTextArea.bind('<Control-O>', self.openFile)
		self.thisTextArea.bind('<Button-1>', self.updateRowsNumber())
		self.thisTextArea.bind('<Button-3>', self.updateRowsNumber())
		self.thisTextArea.bind('<Motion>', self.updateRowsNumber)
		self.thisTextArea.bind('<Key>', self.chkStatusFile)
		self.thisTextArea.bind('<Escape>', self.exit)
		
		self.menu.focus()
		self.menu.add_cascade(label='Nuevo', command=self.newFile)
		self.menu.add_cascade(label='Abrir', command=self.openFile)
		self.menu.add_cascade(label='Guardar', command=self.saveFile)
		self.menu.add_separator()
		self.menu.add_cascade(label='Cerrar', command=self.exit)
		
		
	def newFile(self, event=''):
		self.root.title(self.original_title + self.unsave + self.script)
		self.thisTextArea.delete(1.0, END)
		self._file = None
		self.lineNumber = self.thisTextArea.index('end-1c').split('.')[0]
		self.status.set('Lineas: '+str(self.lineNumber))
	
	def openFile(self, event=''):
		
		text = ''
		self.root.wm_attributes('-topmost', False)
		
		f_name = ex.getFileName(title='Abrir Archvio Tipo ZioN',
								file_types=[['Archivos ZioN','*.zion']])
		
		if f_name:
			self._file = f_name
			self.title = os.path.basename(self._file)
			self.root.title(self.title + self.save + self.script)
			self.thisTextArea.delete(1.0, END)
			
			with open(self._file, 'rb') as f:
				text = f.read()
				text = decode(text).decode()
				while text.endswith('\n'):
					text = text[:-1]
				text += '\n'
				f.close()
			
			self.thisTextArea.insert(1.0, text)
		else:
			self._file = None
		
		self.root.wm_attributes('-topmost', True)
		self.updateRowsNumber()
	
	def saveFile(self, event=''):
		
		self.root.wm_attributes('-topmost', False)
		
		if self._file:
			
			with open(self._file, 'wb') as f:
				text = encode(self.thisTextArea.get(1.0,END).encode())
				f.write(text)
				f.close()
			
			self.root.title(self.title + self.save + self.script)
			
		else:
			
			f_name_s = ex.getFileNameSave(title='Guardar Archvio Tipo ZioN',
									file_types=[['Archivos ZioN','*.zion']])
			if f_name_s:
				
				if not f_name_s.endswith('.zion'):
					if f_name_s.endswith('.')   or f_name_s.endswith('.z')\
					or f_name_s.endswith('.zi') or f_name_s.endswith('.zio'):
						f_name_s = '.'.join(f_name_s.split('.')[:-1])
					
					f_name_s += '.zion'
					if os.path.exists(f_name_s):
						resp = askyesno('Confirmar Guradar como',
											os.path.basename(f_name_s)+\
											' ya existe.\n¿Desea reemplazarlo?')
						if resp == False:
							return
				
				self._file = f_name_s
				
				with open(self._file, 'wb') as f:
					text = encode(self.thisTextArea.get(1.0,END).encode())
					f.write(text)
					f.close()
				
				self.title = os.path.basename(self._file)
				self.root.title(self.title + self.save + self.script)
			else:
				self._file = None
		
		self.root.wm_attributes('-topmost', True)
		self.updateRowsNumber()
	
	# ~ def track_change_to_text(self, event):
		# ~ self.thisTextArea.tag_add("here", "1.0", "1.8")
		# ~ self.thisTextArea.tag_config("here", background="black", foreground="green")
	
	def chkStatusFile(self, event=''):
		self.updateRowsNumber()
		self.root.title(self.title + self.unsave + self.script)
	
	def updateRowsNumber(self, event=''):
		self.rowsNumber = self.thisTextArea.index('end-1c').split('.')[0]
		self.status.set('Filas: '+str(self.rowsNumber))
	
	def popup(self, event):
		self.menu.post(event.x_root, event.y_root)
	
	def exit(self, event=''):
		self.root.destroy()
		Hide(False)
		sys.exit()
	
	def run(self):
		# Corre el programa:
		self.root.mainloop()


# ~ def openFileToRead():
	
	# ~ f_name = ex.getFileName(title='Abrir Archvio Tipo ZioN',
							# ~ file_types=[['Archivos ZioN','*.zion']])
	
	# ~ with open(f_name, 'rb') as f:
		# ~ text = f.read()
		# ~ text = decode(text)
		# ~ f.close()
	
	# ~ return text.decode(), f_name

# ~ def openFileToSave(text):
	
	# ~ f_name_s = ex.getFileNameSave(title='Guardar Archvio Tipo ZioN',
								# ~ file_types=[['Archivos ZioN','*.zion']])
	
	# ~ with open(f_name_s, 'wb') as f:
		# ~ text = encode(text)
		# ~ f.write(text)
		# ~ f.close()
	
	# ~ return f_name_s



if __name__ == '__main__':
	
	# ~ text, f_name = openFileToRead()
	# ~ print('\n\n\t Contenido del Archivo {}:\n\n{}'.format(f_name, text))
	# ~ openFileToSave(text.encode())
	
	# Inicializa:
	notepad = Notepad(width=720,height=480)
	# Corre el programa:
	notepad.run()
	print(True)
	


