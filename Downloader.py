# /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

"""
    Clase que hereda de tkinter.Tk
    GUI del programa
"""

# __author__ = jjr4p

#widgets
from tkinter import Tk, Label, Button, Entry, Text, Listbox, ttk, PhotoImage
#variables
from tkinter import  StringVar
#constantes
from tkinter import DISABLED, VERTICAL

from ttkthemes import ThemedTk

import os
import platform


class Downloader(ThemedTk):

    def __init__(self, controlador, *args, **kwargs):
        """ Constructor de la GUI """
        ThemedTk.__init__(self, *args, *kwargs)
        
        self.controlador = controlador
        self.controlador.vista = self
        self.recurso = None
        self.getScreenSize()
        geometry = "751x688+"
        geometry += str(int(self.ancho/2)-375) + "+"
        geometry += str(int(self.alto/2)-344)
        self.geometry(geometry)
        self.resizable(0, 0)
        self.title("Downloader")
        self.config(bg='white')
        self.iconbitmap('descarga.ico')
        self.set_theme("elegance")
        self.config(bg='#4C4C4D')
        self.iniciaComponentes()

    def iniciaComponentes(self):
        """
                Método encargado de inicializar los componentes
                de la GUI del programa
        """
        # Variables
        self.url = StringVar()
        self.path = StringVar()

        self.notebook = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.notebook, width=747, height=500)
        self.tabPL = ttk.Frame(self.notebook, width=747, height=500)
        self.style = ttk.Style()
        self.style.configure('.', background="#4C4C4D")
        self.style.configure('.', foreground="#000000")
        self.style.configure('.',font="-family {Dejavu Sans} -size 14 -weight normal -slant roman -underline 0 -overstrike 0")
        # Título
        ttk.Label(self, text="Downloader", font=("Arial", 25)).place(x=300, y=10)

        #Cargar urls
        ttk.Label(self, text="Url:", font=("Arial", 14)).place(x=95, y=70)
        self.entrada = ttk.Entry(self, textvariable=self.url, width=60,
                             font=("Arial", 12))
        self.entrada.place(x=135, y=71)
        self.entrada.bind('<Double-Button-1>', self.controlador.copia)
        ttk.Label(self, text="Carpeta:", font=("Arial", 14)).place(x=95, y=100)
        ttk.Entry(self, textvariable=self.path, width=62,
              font=("Arial", 11)).place(x=177, y=101)
        ttk.Button(self, text="...",width=1, command=self.controlador.cambiaPath).place(x=687, y=100)
        self.button = ttk.Button(self, text="Cargar url",
                             command=self.controlador.cargarurl)
        self.button.place(x=270, y=140)
        self.bborrar = ttk.Button(self, text="Borrar url",
                              command=self.controlador.borrarurl)
        self.bborrar.place(x=420, y=140)
        self.iniciaTab1()
        self.iniciaTabPL()

        # Agrega pestañas
        self.notebook.add(self.tab1, text="Video YT")
        self.notebook.add(self.tabPL, text="Playlist YT")
        self.notebook.place(x=1, y=160)

        # Define el path en el directorio actual
        self.path.set(os.getcwd())

    def iniciaTab1(self):
        
        ttk.Label(self.tab1, text="Info de la url:",
              font=("Arial", 15)).place(x=10, y=30)
        self.text = Text(self.tab1, width=39, height=9,
                         font=("Arial", 12), bg='#ABAAAA',
                         wrap='word')
        EventScrollBar = ttk.Scrollbar(
            self.tab1, command=self.text.yview,
            orient="vertical")
        EventScrollBar.place(x=365, y=65, height=166)
        self.text.configure(yscrollcommand=EventScrollBar.set)
        self.text.config(state=DISABLED)
        self.text.place(x=10, y=235-170)
        ttk.Label(self.tab1, text="Imagen:", font=("Arial", 15)
              ).place(x=400, y=30)
        self.imagen = ttk.Label(self.tab1, text="No disponible",
                            font=("Arial", 11))
        self.imagen.place(x=400, y=60)
        ttk.Label(self.tab1, text=" Formatos disponibles: ", font=("Arial", 15)
              ).place(x=10, y=260)

        self.listbox = Listbox(self.tab1, height=5, width=65,
                               font=("Arial", 13), bg='#ABAAAA')
        scrollbar = ttk.Scrollbar(self.tab1, orient=VERTICAL
          , command =self.listbox.yview )
        scrollbar.place(x=660, y=290, height=114)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.config(selectforeground="#eeeeee",
                            selectbackground="#89C2DE",
                            selectborderwidth=1)

        self.listbox.place(x=85, y=290)
        self.bvideo = ttk.Button(self.tab1, text="Descargar video",
                             command=self.controlador.descargaVideo)
        self.bvideo.place(x=210, y=420)
        self.baudio = ttk.Button(self.tab1, text="Descargar audio",
                             command=self.controlador.descargaAudio)
        self.baudio.place(x=420, y=420)

    def iniciaTabPL(self):
        ttk.Label(self.tabPL, text="Videos disponibles: ", 
          font=("Arial", 14)).place(x=5,y=10)
        self.listPL = Listbox(self.tabPL, height=10, width=66,
                               font=("Arial", 14), bg='#ABAAAA')
        scrollbar = ttk.Scrollbar(self.tabPL, 
                  command=self.listPL.yview, orient=VERTICAL)
        self.listPL.config(yscrollcommand=scrollbar.set)
        self.listPL.config(selectforeground="#eeeeee",
                            selectbackground="#89C2DE",
                            selectborderwidth=1)
        self.listPL.place(x=6,y=50)
        scrollbar.place(x=723,y=50, height=254)
        self.plbvideo = ttk.Button(self.tabPL, text="Ir a descargar video",
                             command = self.controlador.cargarInfoDesdePL)
        self.plbvideo.place(x=30, y=320)
        
        self.plbbvideo = ttk.Button(self.tabPL, text="Descargar playlist video")
        self.plbbvideo.place(x=250, y=320)

        self.plbbaudio = ttk.Button(self.tabPL, text="Descargar playlist audio")
        self.plbbaudio.place(x=500, y=320)

    def setControlador(self, controlador):
        """
                Método encargado de definir un controlador
        """
        self.controlador = controlador

    def getScreenSize(self):
        """
                Método encargado de capturar el tamaño de la pantalla
        """
        self.ancho = self.winfo_screenwidth()
        self.alto = self.winfo_screenheight()
