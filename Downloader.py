#__author__=jjr4p
#descarga video y audio de youtube con python

import os
import platform

from tkinter import *

class Downloader(Tk):

	def __init__(self, controlador, *args, **kwargs):
		Tk.__init__(self, *args, *kwargs)
		self.controlador = controlador
		self.recurso = None
		self.getScreenSize()
		self.geometry("750x600+"+str(int(self.ancho/2)-375)+"+"+str(int(self.alto/2)-300))
		self.resizable(0,0)
		self.title("Downloader")
		self.config(bg='#ABAAAA')
		self.iniciaComponentes()
	
	#Método encargado de los diversos componentes del programa
	def iniciaComponentes(self):

		self.url = StringVar()
		
		Label(self, text="Youtube Downloader", font=("Arial",25), fg="#EE0000",bg='#ABAAAA').place(x=235,y=10)
		Label(self, text="Url:", font=("Arial",14),bg='#ABAAAA').place(x=95, y=70)
		Entry(self, textvariable=self.url, width=60, font=("Arial",12)).place(x=135,y=74)
		
		self.button = Button(self, text="Cargar url", fg='#ffffff',bg='#EC5656', font=("Arial",13), command=self.controlador.cargarurl)
		self.button.place(x=290,y=110)

		self.bborrar = Button(self, text="Borrar url",bg='#EC5656', fg='#ffffff', font=("Arial",13), command=self.controlador.borrarurl)
		self.bborrar.place(x=420,y=110)

		Label(self, text="Info de la url:", font=("Arial",13),bg='#ABAAAA').place(x=10, y=160)
		self.text = Text(self, width=39, height=9, font=("Arial",12), wrap='word')
		EventScrollBar= ttk.Scrollbar(self, command=self.text.yview, orient="vertical")
		EventScrollBar.place(x=353, y=196, height=165)
		self.text.configure(yscrollcommand=EventScrollBar.set)
		self.text.config(state=DISABLED)
		self.text.place(x=10,y=195)
		
		Label(self, text="Imagen:", font=("Arial",13),bg='#ABAAAA').place(x=400, y=160)
		self.imagen = Label(self, text="No disponible", bg="CYAN")

		self.imagen.place(x=400, y=190)

		Label(self, text="Disponibles: ", font=("Arial",13),bg='#ABAAAA').place(x=10, y=370)
		scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
		self.listbox = Listbox(self,height=5, width=65 ,font=("Arial",13), yscrollcommand=scrollbar.set)
		self.listbox.config(selectforeground="#ffffff", selectbackground="#55aa00", selectborderwidth=1)
		self.listbox.place(x=85,y=400)
		self.bvideo = Button(self, text="Descargar video", fg='#ffffff',bg='#EC5656', font=("Arial",14), command=self.controlador.descargaVideo)
		self.bvideo.place(x=210, y=530)
		self.baudio = Button(self, text="Descargar audio", fg='#ffffff',bg='#EC5656', font=("Arial",14), command=self.controlador.descargaAudio)
		self.baudio .place(x=420, y=530)

	#Método encargado de definir un controlador
	def setControlador(self, controlador):
		self.controlador = controlador

	#Método encargado de capturar el tamaño de la pantalla 
	def getScreenSize(self):
		self.ancho = self.winfo_screenwidth()
		self.alto = self.winfo_screenheight()
