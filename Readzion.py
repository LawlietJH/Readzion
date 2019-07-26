
# By: LawlietJH
# Readzion v1.0.9
# Python 3

#=======================================================================

__author__ ='LawlietJH'
__version__='v1.0.9'

debbuger = False

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

if not debbuger:
	Hide()

#=======================================================================

# ~ try: import tkinter as tk
# ~ except: import Tkinter as tk

from tkinter import *
from tkinter.messagebox import *
from explorer import Explorer as ex
import base64
import os


#encode = lambda data: base64.urlsafe_b64encode(data.encode())
#decode = lambda data: base64.urlsafe_b64decode(data).decode()

cmd = lambda comando: os.popen(comando).read()
exists = lambda file_name: os.path.exists(file_name)
encode = lambda data: base64.urlsafe_b64encode(data)
decode = lambda data: base64.urlsafe_b64decode(data)



class Notepad: 
	
	class StatusBar(Frame):

		def __init__(self, master):
			Frame.__init__(self, master)
			self.label = Label(self, bg='#002030', fg='#EBEBEB',
								bd=1, relief=SUNKEN, anchor=E,
								justify=RIGHT, font=('Times', '12', 'bold'))
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
	thisTextArea = Text(root, bg='#002045', fg='#EBEBFF', bd=1,
		insertbackground='#B5D5F5', selectbackground='#008080')
	thisMenuBar = Menu(root)
	thisFileMenu = Menu(thisMenuBar, tearoff=0)
	thisScrollBar = Scrollbar(thisTextArea)
	
	rows = StringVar()
	rowsNumber = 1
	_file = None
	c_csf = 0
	c_bs = 0
	
	original_title = 'Sin Nombre'
	title = original_title
	script = 'Readzion'
	unsave = '* (Sin Guardar) - '
	save = ' - '
	b_unsave = True
	guardado = ''
	
	def __init__(self, **kwargs):
		
		try: self.root.wm_iconbitmap('Notepad.ico')
		except: pass
		
		# Tamano de ventana (Por defecto es de 300x300)
		try:
			self.thisWidth = kwargs['width']
			self.thisHeight = kwargs['height']
		except KeyError: pass
		
		# La ventana por encima de todo:
		self.root.wm_attributes('-topmost', True)
		
		# Titulo de la ventana:
		self.root.title(self.title + self.unsave + self.script)
		self.b_unsave = True
		
		# Crea Barra de Estado:
		self.status = self.StatusBar(self.thisTextArea)
		self.status.pack(side=BOTTOM, fill=X)
		self.updateRowsNumber()
		
		# Centrar la ventana:
		screenWidth = self.root.winfo_screenwidth()
		screenHeight = self.root.winfo_screenheight()
		
		# For left-alling, right-allign, top and bottom
		left = (screenWidth // 2) - (self.thisWidth // 2)
		top = (screenHeight // 2) - (self.thisHeight //2)
		self.root.geometry('{}x{}+{}+{}'.format(self.thisWidth,
										self.thisHeight, left, top))
		
		# Para hacer el TextArea auto resizable
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
		
		# Scrollbar se ajustara automaticamente acorde al contenido
		self.thisScrollBar.config(command=self.thisTextArea.yview)
		self.thisTextArea.config(yscrollcommand=self.thisScrollBar.set)
		
		# Otros Eventos:
		self.root.bind('<Button-3>', self.popup)
		self.root.protocol('WM_DELETE_WINDOW', self.exit)
		# ~ self.thisTextArea.bind('<Button-1>', self.updateRowsNumber)
		# ~ self.thisTextArea.bind('<Motion>', self.updateRowsNumber)
		
		# Eventos del teclado:
		self.root.bind('<Escape>', self.exit)
		
		self.thisTextArea.bind('<Control-n>', self.newFile)
		self.thisTextArea.bind('<Control-N>', self.newFile)
		
		self.thisTextArea.bind('<Control-g>', self.saveFile)
		self.thisTextArea.bind('<Control-s>', self.saveFile)
		self.thisTextArea.bind('<Control-G>', self.saveFile)
		self.thisTextArea.bind('<Control-S>', self.saveFile)
		
		self.thisTextArea.bind('<Control-a>', self.openFile)
		self.thisTextArea.bind('<Control-o>', self.openFile)
		self.thisTextArea.bind('<Control-A>', self.openFile)
		self.thisTextArea.bind('<Control-O>', self.openFile)
		
		self.thisTextArea.bind('<Return>', self.intro_pressed)
		self.thisTextArea.bind('<BackSpace>', self.backspace_pressed)
		
		self.thisTextArea.bind('<Key>', self.chkStatusFile)
		# ~ self.thisTextArea.bind('<Enter>', self.)
		# ~ self.thisTextArea.bind('<Leave>', self.)
		
		# ~ self.button = Button(root, text="Destroy", command=root.destroy)
		# ~ self.button.pack()
		
		# Menu PopUp
		self.menu = Menu(self.root, tearoff=0)
		self.menu.focus()
		self.menu.add_cascade(label='Nuevo', command=self.newFile)
		self.menu.add_cascade(label='Abrir', command=self.openFile)
		self.menu.add_cascade(label='Guardar', command=self.saveFile)
		self.menu.add_separator()
		self.menu.add_cascade(label='Cerrar', command=self.exit)
		
		# ~ self.root.after(10000, lambda: self.chkStatusFile())
		
		
	def newFile(self, event=''):
		self.root.title(self.original_title + self.unsave + self.script)
		self.b_unsave = True
		self.thisTextArea.delete(1.0, END)
		self.updateRowsNumber()
		self._file = None
	
	def openFile(self, event=''):
		
		text = ''
		self.root.wm_attributes('-topmost', False)
		
		f_name = ex.getFileName(title='Abrir Archvio Tipo ZioN',
								file_types=[['Archivos ZioN','*.zion']])
		
		if f_name:
			self._file = f_name
			self.title = os.path.basename(self._file)
			self.root.title(self.title + self.save + self.script)
			self.b_unsave = False
			self.thisTextArea.delete(1.0, END)
			
			with open(self._file, 'rb') as f:
				text = f.read()
				text = decode(text).decode()
				while text.endswith('\n'):
					text = text[:-1]
				text += '\n'
				f.close()
			
			self.thisTextArea.insert(1.0, text)
			self.guardado = self.thisTextArea.get(1.0,END)
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
			self.b_unsave = False
			self.guardado = self.thisTextArea.get(1.0,END)
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
				self.b_unsave = False
				self.guardado = self.thisTextArea.get(1.0,END)
			else:
				self._file = None
		
		self.root.wm_attributes('-topmost', True)
		self.updateRowsNumber()
	
	# ~ def track_change_to_text(self, event):
		# ~ self.thisTextArea.tag_add("here", "1.0", "1.8")
		# ~ self.thisTextArea.tag_config("here", background="black", foreground="green")
	def intro_pressed(self, event):
		self.chkStatusFile()
		self.rowsNumber = self.thisTextArea.index('end').split('.')[0]
		self.status.set('Filas: '+self.rowsNumber)
	
	def backspace_pressed(self, event=''):
		self.chkStatusFile()
		val = self.thisTextArea.get(1.0,END).count('\n')
		# ~ cur = self.thisTextArea.index(INSERT)
		self.rowsNumber = str(val)
		self.status.set('Filas: '+self.rowsNumber)
		
		if self.c_bs == 0:
			self.root.after(100, self.backspace_pressed)
			self.c_bs += 1
		else:
			self.c_bs = 0
	
	def chkStatusFile(self, event=''):
		actual = self.thisTextArea.get(1.0,END)
		if not actual == self.guardado:
			self.root.title(self.title + self.unsave + self.script)
			self.b_unsave = True
		else:
			self.root.title(self.title + self.save + self.script)
			self.b_unsave = False
		
		if self.c_csf == 0:
			self.root.after(100, self.chkStatusFile)
			self.c_csf += 1
		else:
			self.c_csf = 0
	
	def updateRowsNumber(self, event=''):
		self.rowsNumber = self.thisTextArea.index('end-1c').split('.')[0]
		self.status.set('Filas: '+self.rowsNumber)
		# ~ self.chkStatusFile()
	
	def popup(self, event):
		self.menu.post(event.x_root, event.y_root)
	
	def exit(self, event=''):
		self.root.wm_attributes('-topmost', False)
		if self.b_unsave == True:
			if askokcancel('Cerrar', 'Desea Salir Sin Guardar?'):
				self.root.destroy()
				Hide(False)
				sys.exit()
			else:
				self.root.wm_attributes('-topmost', True)
		else:
			self.root.destroy()
			Hide(False)
			sys.exit()
	
	def run(self):
		# Corre el programa:
		if not debbuger:
			cmd('mode con cols=30 lines=5')
		self.root.mainloop()



if __name__ == '__main__':
	
	# Inicializa:
	notepad = Notepad(width=720,height=480)
	# Corre el programa:
	notepad.run()
	print(True)
	

