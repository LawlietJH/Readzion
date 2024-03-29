
# By: LawlietJH
# Readzion v1.2.1
# Python 3

#=======================================================================

__author__ ='LawlietJH'
__version__='v1.2.1'

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

from tkinter.messagebox import *
from tkinter.ttk import Progressbar
from tkinter import *

from explorer import Explorer as ex				# Descragar De: github.com/LawlietJH/Explorer
import win32clipboard as WCB					# pip install pywin32
import threading
import base64
import time
import os

#encode = lambda data: base64.urlsafe_b64encode(data.encode())
#decode = lambda data: base64.urlsafe_b64decode(data).decode()

cmd = lambda comando: os.popen(comando).read()
exists = lambda file_name: os.path.exists(file_name)
encode = lambda data: base64.urlsafe_b64encode(data)
decode = lambda data: base64.urlsafe_b64decode(data)
del_file = lambda name: os.remove(name)
file_exists = lambda name: os.path.exists(name)


class Notepad: 
	
	class StatusBar(Frame):

		def __init__(self, master):
			Frame.__init__(self, master)
			self.label = Label(self, bg='#002030', fg='#EBEBEB',
								bd=1, relief=SUNKEN, anchor=E,
								justify=RIGHT, font=('Arial', '10', 'bold'))
			self.label.pack(fill=X)

		def set(self, format, *args):
			self.label.config(text=format % args)
			self.label.update_idletasks()

		def clear(self):
			self.label.config(text='')
			self.label.update_idletasks()
	
	class Clipboard:
		
		def getText():
			WCB.OpenClipboard()
			data = WCB.GetClipboardData()
			WCB.CloseClipboard()
			return data
		
		def setText(cadena):
			WCB.OpenClipboard()
			WCB.EmptyClipboard()
			WCB.SetClipboardText(cadena.encode('utf-8'), WCB.CF_TEXT)
			WCB.CloseClipboard()
		
		def cleanText():
			WCB.OpenClipboard()
			WCB.EmptyClipboard()
			WCB.CloseClipboard()
	
	class CreateToolTip(object):
		'''
		create a tooltip for a given widget
		'''
		def __init__(self, widget, text='widget info'):
			self.widget = widget
			self.tw = None
			self.text = text
			self.widget.bind("<Enter>", self.enter)
			self.widget.bind("<Leave>", self.close)
		def enter(self, event=None):
			# ~ x = y = 0
			# ~ x, y, cx, cy = self.widget.bbox("insert")
			# ~ print(x, y, cx, cy)
			x = event.x_root 
			y = event.y_root
			# creates a toplevel window
			self.tw = Toplevel(self.widget)
			# Leaves only the label and removes the app window
			self.tw.wm_overrideredirect(True)
			self.tw.wm_attributes('-topmost', True)
			self.tw.wm_geometry("+%d+%d" % (x, y))
			label = Label(self.tw, text=self.text, justify='left',
						   background='white', relief='solid', borderwidth=1,
						   font=("times", "8", "normal"))
			label.pack(ipadx=1)
		def close(self, event=None):
			if self.tw:
				self.tw.destroy()
	
	# https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
	# https://stackoverflow.com/questions/55316791/how-can-i-add-a-tooltip-to-menu-item
	# https://likegeeks.com/es/ejemplos-de-la-gui-de-python/
	# https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
	
	#===================================================================
	
	root = Tk()
	
	# La ventana por encima de todo:
	root.wm_attributes('-topmost', True)
	# No se puede cambiar su tamaño: Ancho y Alto.
	# ~ root.resizable(width=True, height=False)
	
	# Siempre en equina superior izquierda:
	# ~ root.overrideredirect(True)
	
	# ~ root.lift()
	# ~ root.wm_attributes('-transparentcolor', 'white')
	
	thisWidth = 600
	thisHeight = 400
	
	_cache_z = []
	_cache_y = []
	
	#===================================================================
	
	# Pagina de colores: https://mycolor.space/?hex=%23002045&sub=1
	thisTextArea = Text(root, bg='#002045', fg='#EBEBFF', bd=1,
		insertbackground='#B5D5F5', selectbackground='#008080',
		wrap=CHAR)		#wrap = NONE, CHAR or WORD
	thisScrollBarY = Scrollbar(thisTextArea)
	thisScrollBarX = Scrollbar(thisTextArea, orient=HORIZONTAL)
	
	#===================================================================
	
	bg_menu = '#004080'
	fg_menu = '#EBEBFF'
	
	thisMenuBar = Menu(root, bg=bg_menu, fg=fg_menu)
	
	#===================================================================
	
	popUp = Menu(root, tearoff=0, bg=bg_menu, fg=fg_menu)
	popUpF = Menu(popUp, tearoff=0, bg=bg_menu, fg=fg_menu)
	
	#===================================================================
	
	eliminar_state = False
	vaciar_state = False
	encima_state = False
	
	rowsNumber = 1
	_file = None
	c_clip = 0
	c_csf = 0
	c_bs = 0
	
	l_base64 = []
	
	#===================================================================
	
	cur_c_pos     = '1.0'	# Current cursor position in the text 'line.column'
	cur_c_char    = '\n'	# Current cursor position char in the text 'a'
	cur_s_text    = ''		# Current selection text in text 'abcdefg...'
	cur_s_pos_ini = ''		# Current cursor init position in selected text 'line.column'
	cur_s_pos_end = ''		# Current cursor end position in selected text 'line.column'
	
	current_cursor = [cur_c_pos, cur_c_char, cur_s_text, cur_s_pos_ini, cur_s_pos_end]
	
	#===================================================================
	
	original_title = 'Sin Nombre'
	title = original_title
	script = 'Readzion ' + __version__
	unsave = '* (Sin Guardar) - '
	save = ' - '
	b_unsave = True
	guardado = None
	modo_lectura = False
	
	progress = IntVar()
	progress = 0
	bar = None
	
	def __init__(self, **kwargs):
		
		try:
			self.root.wm_iconbitmap('Readzion.ico')
			# ~ self.root.wm_iconphoto(True, tk.PhotoImage(file='Readzion.ico'))
		except: pass
		
		# Tamano de ventana (Por defecto es de 600x400)
		try:
			self.thisWidth = kwargs['width']
			self.thisHeight = kwargs['height']
		except KeyError: pass
		
		# ~ self.progressbar()
		
		# ~ bar = threading.Thread(target=self.progressbar)
		# ~ bar.setName('StartProgressBar')
		# ~ bar.start()
		
		# Titulo de la ventana:
		self.root.title(self.title + self.unsave + self.script)
		self.b_unsave = True
		
		# Crea Barra de Estado:
		self.status = self.StatusBar(self.thisTextArea)
		self.status.pack(side=BOTTOM, fill=X)
		self.chkStatusFile()
		
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
		self.thisTextArea.focus()
		self.thisScrollBarY.pack(side=RIGHT, fill=Y)
		self.thisScrollBarX.pack(side=BOTTOM, fill=X)
		self.thisScrollBarY.config(command=self.thisTextArea.yview)			# Scrollbar se ajustara automaticamente acorde al contenido
		self.thisScrollBarX.config(command=self.thisTextArea.xview)			# Scrollbar se ajustara automaticamente acorde al contenido
		self.thisTextArea.config(yscrollcommand=self.thisScrollBarY.set,
								xscrollcommand=self.thisScrollBarX.set)
		
		# ~ self.ttp = self.CreateToolTip(self.thisTextArea, 'mouse is over button 1')
		# ~ self.ttp.close()
		
		# Menus: =======================================================
		
		# Barra de Menu:
		self.barra_menu()
		
		# Menu PopUp
		self.popup_menu()
		
		#===============================================================
		
		# Otros Eventos:
		# ~ self.thisTextArea.bind('<Button-1>', self.updateCurrentCursor)
		self.root.bind('<Button-3>', self.popup)
		# ~ self.root.bind('<Motion>', self.chkpositions)
		self.root.protocol('WM_DELETE_WINDOW', self.exit)
		self.thisTextArea.bind('<Motion>', self.updateCurrentCursor)
		# Eventos del teclado:
		self.bind_keys()
		
		
		# ~ self.button = Button(root, text='Destroy', command=root.destroy)
		# ~ self.button.pack()
		
		# ~ self.root.after(10000, lambda: self.chkStatusFile())
	
	
	# ~ def chkpositions(self, event):
		
		# ~ print(self.root.winfo_x(), self.root.winfo_y())
		# ~ print(event.x_root, event.y_root)
		
	
	#===================================================================
	#===================================================================
	#===================================================================
	
	def progressbar(self):
		
		self.bp = Toplevel(self.root)
		# ~ self.bp.title('Barra de Progreso')
		# ~ self.bp.attributes("-toolwindow",-1)
		self.bp.wm_attributes('-topmost', True)
		self.bp.overrideredirect(1)
		
		left = int(self.root.winfo_screenwidth()/2 - 300)
		top = int(self.root.winfo_screenheight()/2 - 200)
		
		self.bp.geometry('+{}+{}'.format(left, top))
		
		self.bar = Progressbar(self.bp, length=200, variable=self.progress)
		self.bar.place(x=30, y=60)
		self.bar.pack()
	
	def cache(self, event=None):
		
		if event:
			# ~ print(event.keysym)
			if 'Control' in event.keysym or 'Alt' in event.keysym\
			or 'Win' in event.keysym or 'Caps' in event.keysym\
			or event.keysym in ['Up', 'Down', 'Left', 'Right']\
			or event.keysym in ['F1','F2','F3','F4', 'F5', 'F6']\
			or event.keysym in ['F7','F8','F9','F10','F11','F12']\
			or 'Shift' in event.keysym:
				return
			
		texto = self.thisTextArea.get(1.0,END)[:-1]
		
		if not self._cache_z == []:
			if not self._cache_z[-1] == texto:
				self._cache_z.append(texto)
				# ~ print(self._cache_y)
				self._cache_y = []
		else:
			self._cache_z.append(texto)
	
	def c_zeta(self, event=None):
		
		if not self._cache_z == []:
			
			texto = self.thisTextArea.get(1.0,END)[:-1]
			val = self._cache_z.pop()
			
			if val == texto and not self._cache_z == []:
				val = self._cache_z.pop()
			
			self._cache_y.append(texto)
			self.thisTextArea.delete(1.0, END)
			self.thisTextArea.insert(1.0, val)
			
			self.updateCurrentCursor()
		
	def c_ye(self, event=None):
		
		if not self._cache_y == []:
			
			texto = self.thisTextArea.get(1.0,END)[:-1]
			val = self._cache_y.pop()
			
			if val == texto and not self._cache_y == []:
				val = self._cache_y.pop()
			
			self._cache_z.append(texto)
			self.thisTextArea.delete(1.0, END)
			self.thisTextArea.insert(1.0, val)
			
			self.updateCurrentCursor()
		
	#===================================================================
	#===================================================================
	#===================================================================
	
	def barra_menu(self):
		
		self.thisFileMenu = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		self.thisEnableMenu = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		self.thisLineTextMenu = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		self.thisSubLineText = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		self.thisCipherMenu = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		# ~ self.thisCipherAESMenu = Menu(self.thisMenuBar, tearoff=0, bg=self.bg_menu, fg=self.fg_menu)
		
		# Archivo:
		self.thisFileMenu.add_command(label='Nuevo', underline=0, accelerator='Ctrl+N', command=self.newFile)
		self.thisFileMenu.add_command(label='Abrir', underline=0, accelerator='Ctrl+O', command=self.openFile)
		self.thisFileMenu.add_command(label='Guardar', underline=0, accelerator='Ctrl+G / Ctrl+S', command=self.saveFile)
		self.thisFileMenu.add_command(label='Guardar Como', underline=1, accelerator='Ctrl+U', command=self.saveFileAs)
		self.thisFileMenu.add_separator()
		self.thisFileMenu.add_command(label='Eliminar Archivo', underline=1, state='disabled', command=self.delFile)
		self.thisFileMenu.add_command(label='Vaciar Archivo', underline=0, state='disabled', command=self.cleanFile)
		self.thisFileMenu.add_separator()
		self.thisFileMenu.add_command(label='Cerrar', underline=0, accelerator='Esc', command=self.exit)
		
		# Habilitar:
		self.thisEnableMenu.add_checkbutton(label='Siempre Encima', underline=0, command=self.encimar)
		self.thisEnableMenu.add_checkbutton(label='Eliminar', underline=0, command=self.habilitarEliminar)
		self.thisEnableMenu.add_checkbutton(label='Vaciar', underline=0, command=self.habilitarVaciar)
		self.thisEnableMenu.add_checkbutton(label='Modo Lectura', underline=0, command=self.modoLectura)
		self.thisEnableMenu.invoke(0)
		
		# Formato:
		self.thisSubLineText.add_radiobutton(label='Por Caracter', underline=0, command=lambda: self.thisTextArea.config(wrap=CHAR))
		self.thisSubLineText.add_radiobutton(label='De Forma Continua', underline=0, command=lambda: self.thisTextArea.config(wrap=NONE))
		self.thisSubLineText.add_radiobutton(label='Por Palabra', underline=0, command=lambda: self.thisTextArea.config(wrap=WORD))
		self.thisLineTextMenu.add_cascade(label='Ajuste de línea', underline=0, menu=self.thisSubLineText)
		self.thisSubLineText.invoke(0)
		
		# Cifrar:
		self.thisCipherMenu.add_command(label='Base64', underline=0, command=self.setBase64)
		# ~ self.thisCipherAESMenu.add_command(label='Encriptar', underline=0, command=self.AES256Encript)
		# ~ self.thisCipherAESMenu.add_command(label='Desencriptar', underline=0, command=self.AES256Decript)
		# ~ self.thisCipherMenu.add_cascade(label='AES 256', underline=0, menu=self.thisCipherAESMenu)
		
		# Activar Menu:
		self.thisMenuBar.add_cascade(label='Archivo', underline=0, accelerator='Alt+A', menu=self.thisFileMenu)
		self.thisMenuBar.add_cascade(label='Habilitar', underline=0, accelerator='Alt+H', menu=self.thisEnableMenu)
		self.thisMenuBar.add_cascade(label='Formato', underline=0, accelerator='Alt+F', menu=self.thisLineTextMenu)
		self.thisMenuBar.add_cascade(label='Cifrar', underline=0, accelerator='Alt+C', menu=self.thisCipherMenu)
		self.root.config(menu=self.thisMenuBar)
	
	def popup_menu(self):
		
		self.popUp.focus()
		self.popUp.add_command(label='Nuevo', command=self.newFile)
		self.popUp.add_command(label='Abrir', command=self.openFile)
		self.popUp.add_command(label='Guardar', command=self.saveFile)
		self.popUp.add_command(label='Guardar Como', command=self.saveFileAs)
		self.popUp.add_separator()
		self.popUpF.add_command(label='Eliminar Archivo', state='disabled', command=self.delFile)
		self.popUpF.add_command(label='Vaciar Archivo', state='disabled', command=self.cleanFile)
		self.popUp.add_cascade(label='Archivo', menu=self.popUpF)
		self.popUp.add_separator()
		self.popUp.add_cascade(label='Cerrar', command=self.exit)
	
	def bind_keys(self):
		
		# Eventos del teclado:
		self.root.bind('<Escape>', self.exit)
		
		self.thisTextArea.bind('<Control-z>', self.c_zeta)
		self.thisTextArea.bind('<Control-Z>', self.c_zeta)
		self.thisTextArea.bind('<Control-y>', self.c_ye)
		self.thisTextArea.bind('<Control-Y>', self.c_ye)
		
		self.thisTextArea.bind('<Control-x>', self.cut_paste)
		self.thisTextArea.bind('<Control-v>', self.cut_paste)
		self.thisTextArea.bind('<Control-X>', self.cut_paste)
		self.thisTextArea.bind('<Control-V>', self.cut_paste)
		
		self.thisTextArea.bind('<Control-n>', self.newFile)
		self.thisTextArea.bind('<Control-N>', self.newFile)
		
		self.thisTextArea.bind('<Control-o>', self.openFile)
		self.thisTextArea.bind('<Control-O>', self.openFile)
		
		self.thisTextArea.bind('<Control-g>', self.saveFile)
		self.thisTextArea.bind('<Control-s>', self.saveFile)
		self.thisTextArea.bind('<Control-G>', self.saveFile)
		self.thisTextArea.bind('<Control-S>', self.saveFile)
		
		self.thisTextArea.bind('<Control-u>', self.saveFileAs)
		self.thisTextArea.bind('<Control-U>', self.saveFileAs)
		
		# ~ self.thisTextArea.bind('<Control-v>', self.chkPaste)
		# ~ self.thisTextArea.bind('<Control-V>', self.chkPaste)
		# ~ self.thisTextArea.bind('<Control-c>', self.chkPaste)
		# ~ self.thisTextArea.bind('<Control-C>', self.chkPaste)
		
		self.thisTextArea.bind('<Return>', self.intro_pressed)
		self.thisTextArea.bind('<BackSpace>', self.backspace_pressed)
		
		self.thisTextArea.bind('<Key>', self.chkStatusFile)
		# ~ self.thisTextArea.bind('<Enter>', self.)
		# ~ self.thisTextArea.bind('<Leave>', self.)
	
	#===================================================================
	#===================================================================
	#===================================================================
	
	# Menu > Archivo:
	
	def newFile(self, event=None):
		self.chkStatusFile()
		texto = self.thisTextArea.get(1.0,END)[:-1]
		if self.b_unsave:
			
			resp = ''
			
			self.root.wm_attributes('-topmost', False)
			
			if self._file:
				resp = askyesno('Confirmar Guardar Cambios',
					'Desea Guardar los Cambios en el Archivo '+\
					os.path.basename(self._file))
			else:
				resp = askyesno('Confirmar Guardar Cambios',
					'Desea Guardar el Archivo?')
				
			if resp:
				self.saveFile()
			
			self.root.title(self.original_title + self.unsave + self.script)
			self.thisTextArea.delete(1.0, END)
			self.title = self.original_title
			self.chkStatusFile()
			self.b_unsave = True
			self._file = None
			self.guardado = None
			
			self.root.wm_attributes('-topmost', self.encima_state)
			
		else:
			self.root.title(self.original_title + self.unsave + self.script)
			self.thisTextArea.delete(1.0, END)
			self.title = self.original_title
			self.chkStatusFile()
			self.b_unsave = True
			self._file = None
			self.guardado = None
		
		self._cache_y = []
		self._cache_z = [texto] + (['']*25)
	
	def openFile(self, event=None):
		self.chkStatusFile()
		self.root.wm_attributes('-topmost', False)
		
		if self.b_unsave:
			
			resp = ''
			
			if self._file:
				resp = askyesno('Confirmar Guardar Cambios',
					'Desea Guardar los Cambios en el Archivo '+\
					os.path.basename(self._file))
			else:
				resp = askyesno('Confirmar Guardar Cambios',
					'Desea Guardar el Archivo?')
				
			if resp:
				self.saveFile()
		
		text = ''
		f_name = ex.getFileName(title='Abrir Archivo Tipo ZioN',
								file_types=[['Archivos ZioN','*.zion']])
		
		if f_name:
			
			with open(f_name, 'rb') as f:
				
				text = f.read()
				
				try:
					text = decode(text).decode()
				except base64.binascii.Error:
					showwarning('No se pudo Abrir el Documento',
						'Documento: '+os.path.basename(f_name)+\
						'\nTiene una Codificacion Desconocida o esta Dañado')
					return
				
				while text.endswith('\n'):
					text = text[:-1]
				text += '\n'
				f.close()
			
			self._file = f_name
			self.title = os.path.basename(self._file)
			self.root.title(self.title + self.save + self.script)
			self.thisTextArea.delete(1.0, END)
			self.b_unsave = False
			
			self.thisTextArea.insert(1.0, text)
			self.guardado = self.thisTextArea.get(1.0,END)
			self._cache_y = []
			self._cache_z = []
		else:
			self._file = None
		
		self.root.wm_attributes('-topmost', self.encima_state)
		self.chkStatusFile()
	
	def saveFile(self, event=None):
		
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
			
			f_name_s = ex.getFileNameSave(title='Guardar Archivo Tipo ZioN',
									file_types=[['Archivos ZioN','*.zion']])
			if f_name_s:
				
				if not f_name_s.endswith('.zion'):
					if f_name_s.endswith('.')   or f_name_s.endswith('.z')\
					or f_name_s.endswith('.zi') or f_name_s.endswith('.zio'):
						f_name_s = '.'.join(f_name_s.split('.')[:-1])
					
					f_name_s += '.zion'
					if os.path.exists(f_name_s):
						resp = askyesno('Confirmar Guardado',
											os.path.basename(f_name_s)+\
											' ya existe.\n¿Desea Reemplazarlo?')
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
		
		self.root.wm_attributes('-topmost', self.encima_state)
		self.chkStatusFile()
	
	def saveFileAs(self, event=None):
		self.root.wm_attributes('-topmost', False)
		f_name_s = ex.getFileNameSave(title='Guardar Como Archivo Tipo ZioN',
								file_types=[['Archivos ZioN','*.zion']])
		if f_name_s:
			
			if not f_name_s.endswith('.zion'):
				if f_name_s.endswith('.')   or f_name_s.endswith('.z')\
				or f_name_s.endswith('.zi') or f_name_s.endswith('.zio'):
					f_name_s = '.'.join(f_name_s.split('.')[:-1])
				
				f_name_s += '.zion'
				if os.path.exists(f_name_s):
					resp = askyesno('Confirmar Guardar Como',
										os.path.basename(f_name_s)+\
										' ya existe.\n¿Desea Reemplazarlo?')
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
		
		self.root.wm_attributes('-topmost', self.encima_state)
		self.chkStatusFile()
	
	def delFile(self, event=None):
		
		if self._file:
			self.root.wm_attributes('-topmost', False)
			
			resp = askyesno('Confirmar Eliminar Archivo',
				' Esta seguro de Eliminar el Archivo '+os.path.basename(self._file))
			
			if resp:
				del_file(self._file)
				self.newFile()
				self.habilitarEliminar()
			
			self.root.wm_attributes('-topmost', self.encima_state)
	
	def cleanFile(self, event=None):
		
		if self._file:
			
			self.root.wm_attributes('-topmost', False)
			
			resp = askyesno('Confirmar Vaciar Archivo',
				' Esta seguro de Vaciar el Archivo '+os.path.basename(self._file))
			
			if resp:
				self.thisTextArea.delete(1.0, END)
				self.saveFile()
				self.habilitarVaciar()
			
			self.root.wm_attributes('-topmost', self.encima_state)
	
	#===================================================================
	#===================================================================
	#===================================================================
	
	# Menu > Habilitar:
	
	def encimar(self, event=None):
		
		if self.encima_state == True:
			self.encima_state = False
		else:
			self.encima_state = True
		
		self.root.wm_attributes('-topmost', self.encima_state)
	
	def habilitarEliminar(self, event=None):
		
		if self.eliminar_state==True:
			self.eliminar_state=False
		else:
			self.eliminar_state=True
		
		self.popUpF.entryconfig(index='Eliminar Archivo', state='active' if self.eliminar_state else 'disabled')
		self.thisFileMenu.entryconfig(index='Eliminar Archivo', state='active' if self.eliminar_state else 'disabled')
	
	def habilitarVaciar(self, event=None):
		
		if self.vaciar_state==True:
			self.vaciar_state=False
		else:
			self.vaciar_state=True
		
		self.popUpF.entryconfig(index='Vaciar Archivo', state='active' if self.vaciar_state else 'disabled')
		self.thisFileMenu.entryconfig(index='Vaciar Archivo', state='active' if self.vaciar_state else 'disabled')
	
	def modoLectura(self, event=None):
		
		if self.modo_lectura:
			self.thisTextArea.config(state='normal')
			self.modo_lectura = False
		else:
			self.thisTextArea.config(state='disable')
			self.modo_lectura = True
	
	#===================================================================
	#===================================================================
	#===================================================================
	
	# Menu > Cifrado:
	
	def setBase64(self):	# Cifra el texto seleccionado.
		
		# chache() permite hacer Ctrl+Z a un texto cifrado y recuperar texto.
		# Y Posteriormente tambien permite el uso de Ctrl+Y.
		self.cache()
		
		xD = True
		s_code = ''
		s_text = self.current_cursor[2]		# texto seleccionado.
		if s_text != '':
			for t, e in self.l_base64:
				if s_text == t:
					xD = False
					s_code = e
					break
			
			if xD:
				try:
					s_code = decode(s_text).decode()
				except:
					s_code = encode(s_text.encode())
				
				self.l_base64.append((s_text, s_code))
			
			pos_i, pos_f = self.current_cursor[3:5]
			
			if pos_i != '':
				self.thisTextArea.delete(pos_i, pos_f)
				self.thisTextArea.insert(pos_i, s_code)
	
	def AES256Decript(self):
		
		self.cache()
		
		# ~ cifrar = AES(password)
		
		s_code = ''
		s_text = self.current_cursor[2]		# texto seleccionado.
		if s_text != '':
			
			# ~ s_code = decrypted = cifrar.desencriptar(s_text)
			
			pos_i, pos_f = self.current_cursor[3:5]
			
			if pos_i != '':
				self.thisTextArea.delete(pos_i, pos_f)
				self.thisTextArea.insert(pos_i, s_code)
		
	def AES256Encript(self):
		
		self.cache()
		
		# ~ cifrar = AES(password)
		
		s_code = ''
		s_text = self.current_cursor[2]		# texto seleccionado.
		if s_text != '':
			
			# ~ s_code = encrypted = cifrar.encriptar(s_text)
			
			pos_i, pos_f = self.current_cursor[3:5]
			
			if pos_i != '':
				self.thisTextArea.delete(pos_i, pos_f)
				self.thisTextArea.insert(pos_i, s_code)
		
	#===================================================================
	#===================================================================
	#===================================================================
	
	def chkStatusFile(self, event=None):
		
		# ~ self.progress += 1
		# ~ self.bar['value'] = self.progress
		
		if self._file and not file_exists(self._file):
			self.root.title(self.title + self.unsave + self.script)
			self.b_unsave = True
		else:
			actual = self.thisTextArea.get(1.0,END)
			if not actual == self.guardado:
				self.root.title(self.title + self.unsave + self.script)
				self.b_unsave = True
			else:
				self.root.title(self.title + self.save + self.script)
				self.b_unsave = False
		
		if self.c_csf == 0:
			self.cache(event)
			self.root.after(100, self.chkStatusFile)
			self.c_csf += 1
		else:
			self.c_csf = 0
		
		self.updateCurrentCursor()
	
	def chkPaste(self, event=None):
		self.chkStatusFile()
		self.rowsNumber = self.thisTextArea.index('end-1c').split('.')[0]
		self.updateStatusBar()
		# ~ SG9sYSB4RA== --> Hola xD
		try:
			c_text = self.Clipboard.getText()
		except:
			print('Error')
			return
		
		if c_text != '':
			
			try: c_text = decode(c_text).decode()
			except: pass
			
			self.Clipboard.setText(c_text)
			
			if self.c_clip == 0:
				self.root.after(100, self.chkPaste)
				self.c_clip += 1
			else:
				self.c_clip = 0
	
	def updateCurrentCursor(self, event=None):
		
		clip = ''
		self.cur_c_pos  = self.thisTextArea.index(INSERT)
		self.cur_c_char = self.thisTextArea.get(INSERT)
		
		try:
			self.cur_s_text    = self.thisTextArea.selection_get()
			self.cur_s_pos_ini = self.thisTextArea.index(SEL_FIRST)
			self.cur_s_pos_end = self.thisTextArea.index(SEL_LAST)
		except TclError:
			self.cur_s_text    = ''
			self.cur_s_pos_ini = ''
			self.cur_s_pos_end = ''
		try:
			clip = self.root.clipboard_get()
		except TclError:
			clip = ''
		
		self.current_cursor = [
				self.cur_c_pos,
				self.cur_c_char,
				self.cur_s_text,
				self.cur_s_pos_ini,
				self.cur_s_pos_end,
				clip
			]
		
		# ~ print(self.current_cursor)
		self.rowsNumber = self.thisTextArea.index('end-1c').split('.')[0]
		self.updateStatusBar()
	
	def updateStatusBar(self):
		line, col = self.current_cursor[0].split('.')
		self.status.set('|   Línea {}, Col {}   |  Filas: {:<6}'.format(
			int(line), int(col)+1, self.rowsNumber))
	
	def cut_paste(self, event=None):
		if self.c_bs == 0:
			self.root.after(100, self.cut_paste)
			self.c_bs += 1
		else:
			self.c_bs = 0
			
		self.chkStatusFile()
	
	def intro_pressed(self, event):
		self.chkStatusFile()
		# ~ self.rowsNumber = self.thisTextArea.index('end').split('.')[0]
		# ~ self.updateStatusBar()
	
	def backspace_pressed(self, event=None):
		self.chkStatusFile()
		# ~ val = self.thisTextArea.get(1.0,END).count('\n')
		# ~ #cur = self.thisTextArea.index(INSERT)
		# ~ self.rowsNumber = str(val)
		# ~ self.updateStatusBar()
		
		if self.c_bs == 0:
			self.root.after(100, self.backspace_pressed)
			self.c_bs += 1
		else:
			self.c_bs = 0
	
	def popup(self, event):
		self.popUp.post(event.x_root, event.y_root)
	
	def exit(self, event=None):
		self.root.wm_attributes('-topmost', False)
		if self.b_unsave == True:
			if askokcancel('Cerrar', 'Desea Salir Sin Guardar?'):
				self.root.destroy()
				Hide(False)
				sys.exit()
			else:
				self.root.wm_attributes('-topmost', self.encima_state)
		else:
			self.root.destroy()
			Hide(False)
			sys.exit()
	
	#===================================================================
	#===================================================================
	#===================================================================
	
	# ~ def track_change_to_text(self, event=None):
		# ~ content = 'Hola :3'
		# ~ #self.thisTextArea.tag_add('here', '1.0', '1.8')
		# ~ #self.thisTextArea.tag_config('here', background='black', foreground='green')
		# ~ text.tag_config("back", background="yellow", foreground="red")
		# ~ text.tag_config("fore", foreground="blue")
		# ~ text.insert(contents, ("back", "fore"))
	
	# ~ def copyText(self, event=None):
		# ~ text = self.thisTextArea.get(SEL_FIRST, SEL_LAST)
		# ~ self.clipboard_clear()
		# ~ self.clipboard_append(text)
	
	# ~ def cutText(self, event=None):
		# ~ self.copyText()
		# ~ self.thisTextArea.delete(SEL_FIRST, SEL_LAST)
	
	# ~ def pasteText(self, event=None):
		# ~ text = self.thisTextArea.selection_get(selection='CLIPBOARD')
		# ~ self.thisTextArea.insert('insert', text)
	
	#===================================================================
	#===================================================================
	#===================================================================
	
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
