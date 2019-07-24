# /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

"""
    Clase que hereda de tkinter.Tk
    GUI del programa
"""

# __author__=jjr4p

from tkinter import *
from tkinter import ttk
import os
import platform


class Downloader(Tk):

    def __init__(self, controlador, *args, **kwargs):
        """ Constructo de la GUI """
        Tk.__init__(self, *args, *kwargs)
        self.controlador = controlador
        self.controlador.vista = self
        self.recurso = None
        self.getScreenSize()
        geometry = "751x688+"
        geometry += str(int(self.ancho/2)-375) + "+"
        geometry += str(int(self.alto/2)-345)
        self.geometry(geometry)
        self.resizable(0, 0)
        self.title("Downloader")
        self.config(bg='#eeeeee')
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

        # Título
        Label(self, text="Youtube Downloader", font=("Arial", 25),
              bg='#eeeeee', fg='#EC5656').place(x=250, y=10)

        #Cargar urls
        Label(self, text="Url:", font=("Arial", 14),
              bg='#eeeeee').place(x=95, y=70)
        self.entrada = Entry(self, textvariable=self.url, width=60,
                             font=("Arial", 12), bg='#ABAAAA')
        self.entrada.place(x=135, y=74)
        self.entrada.bind('<Double-Button-1>', self.controlador.copia)
        Label(self, text="Carpeta:", font=("Arial", 14),
              bg='#eeeeee').place(x=95, y=100)
        Entry(self, textvariable=self.path, width=62,
              font=("Arial", 11), bg='#ABAAAA').place(x=177, y=104)
        Button(self, text="...", command=self.controlador.cambiaPath,
               fg='#eeeeee', bg='#EC5656', font=("Arial", 12, 'bold'),
               width=2, height=1).place(x=685, y=100)
        self.button = Button(self, text="Cargar url", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 13),
                             command=self.controlador.cargarurl)
        self.button.place(x=270, y=140)
        self.bborrar = Button(self, text="Borrar url", bg='#EC5656',
                              fg='#eeeeee', font=("Arial", 13),
                              command=self.controlador.borrarurl)
        self.bborrar.place(x=420, y=140)
        self.iniciaTab1()
        self.iniciaTabPL()

        # Agrega pestañas
        self.notebook.add(self.tab1, text="Video")
        self.notebook.add(self.tabPL, text="Playlist")
        self.notebook.place(x=1, y=160)

        # Define el path en el directorio actual
        self.path.set(os.getcwd())

    def iniciaTab1(self):
        
        Label(self.tab1, text="Info de la url:",
              font=("Arial", 15),
              bg='#eeeeee').place(x=10, y=30)
        self.text = Text(self.tab1, width=39, height=9,
                         font=("Arial", 12), bg='#ABAAAA',
                         wrap='word')
        EventScrollBar = ttk.Scrollbar(
            self.tab1, command=self.text.yview,
            orient="vertical")
        EventScrollBar.place(x=353, y=236-170, height=165)
        self.text.configure(yscrollcommand=EventScrollBar.set)
        self.text.config(state=DISABLED)
        self.text.place(x=10, y=235-170)
        Label(self.tab1, text="Imagen:", font=("Arial", 15),
              bg='#eeeeee').place(x=400, y=30)
        self.imagen = Label(self.tab1, text="No disponible",
                            font=("Arial", 11), bg="#ABAAAA")
        self.imagen.place(x=400, y=60)
        Label(self.tab1, text=" Formatos disponibles: ", font=("Arial", 15),
              bg='#eeeeee').place(x=10, y=260)

        self.listbox = Listbox(self.tab1, height=5, width=65,
                               font=("Arial", 13), bg='#ABAAAA')
        scrollbar = ttk.Scrollbar(self.tab1, orient=VERTICAL
          , command =self.listbox.yview )
        scrollbar.place(x=660, y=290, height=110)
        
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.config(selectforeground="#eeeeee",
                            selectbackground="#55aa00",
                            selectborderwidth=1)
        self.listbox.place(x=85, y=290)
        self.bvideo = Button(self.tab1, text="Descargar video", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14),
                             command=self.controlador.descargaVideo)
        self.bvideo.place(x=210, y=420)
        self.baudio = Button(self.tab1, text="Descargar audio", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14),
                             command=self.controlador.descargaAudio)
        self.baudio.place(x=420, y=420)

    def iniciaTabPL(self):
        Label(self.tabPL, text="Videos disponibles: ", 
          font=("Arial", 14)).place(x=5,y=10)
        self.listPL = Listbox(self.tabPL, height=10, width=66,
                               font=("Arial", 14), bg='#ABAAAA')
        scrollbar = ttk.Scrollbar(self.tabPL, 
                  command=self.listPL.yview, orient=VERTICAL)
        self.listPL.config(yscrollcommand=scrollbar.set)
        self.listPL.config(selectforeground="#eeeeee",
                            selectbackground="#55aa00",
                            selectborderwidth=1)
        self.listPL.place(x=6,y=50)
        scrollbar.place(x=720,y=51, height=250)
        self.plbvideo = Button(self.tabPL, text="Ir a descargar video", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14))
        self.plbvideo.place(x=30, y=320)
        
        self.plbbvideo = Button(self.tabPL, text="Descargar playlist video", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14))
        self.plbbvideo.place(x=250, y=320)

        self.plbbaudio = Button(self.tabPL, text="Descargar playlist audio", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14))
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
