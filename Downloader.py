# /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-


"""
    Clase que hereda de tkinter.Tk
    GUI del programa
"""

# __author__=jjr4p

from tkinter import *
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
        geometry = "750x650+"
        geometry += str(int(self.ancho/2)-375) + "+"
        geometry += str(int(self.alto/2)-325)
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
        self.url = StringVar()
        self.path = StringVar()
        Label(self, text="Youtube Downloader", font=("Arial", 25),
              fg="#EE0000",
              bg='#eeeeee').place(x=255, y=10)
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
        Label(self, text="Info de la url:",
              font=("Arial", 15),
              bg='#eeeeee').place(x=10, y=200)
        self.text = Text(self, width=39, height=9,
                         font=("Arial", 12), bg='#ABAAAA',
                         wrap='word')
        EventScrollBar = ttk.Scrollbar(
            self, command=self.text.yview,
            orient="vertical")
        EventScrollBar.place(x=353, y=236, height=165)
        self.text.configure(yscrollcommand=EventScrollBar.set)
        self.text.config(state=DISABLED)
        self.text.place(x=10, y=235)
        Label(self, text="Imagen:", font=("Arial", 15),
              bg='#eeeeee').place(x=400, y=200)
        self.imagen = Label(self, text="No disponible",
                            font=("Arial", 11), bg="#ABAAAA")
        self.imagen.place(x=400, y=230)
        Label(self, text=" Videos disponibles: ", font=("Arial", 15),
              bg='#eeeeee').place(x=10, y=410)
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self, height=5, width=65,
                               font=("Arial", 13), bg='#ABAAAA',
                               yscrollcommand=scrollbar.set)
        self.listbox.config(selectforeground="#eeeeee",
                            selectbackground="#55aa00",
                            selectborderwidth=1)
        self.listbox.place(x=85, y=440)
        self.bvideo = Button(self, text="Descargar video", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14),
                             command=self.controlador.descargaVideo)
        self.bvideo.place(x=210, y=570)
        self.baudio = Button(self, text="Descargar audio", fg='#eeeeee',
                             bg='#EC5656', font=("Arial", 14),
                             command=self.controlador.descargaAudio)
        self.baudio .place(x=420, y=570)
        self.path.set(os.getcwd())

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
