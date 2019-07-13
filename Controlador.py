# /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

"""
    Clase que controla los eventos del downloader
    además de las descargas de los videos y audios
"""

# __author__=jjr4p

from io import BytesIO
from PIL import ImageTk
from PIL.Image import open as opp
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk
from tkinter import filedialog
import pafy
import requests
import os
import threading
import platform


class Controlador:

    def setVista(self, vista):
        """ Define la vista que será controlada """
        self.vista = vista
        self.recurso = None

    def cargarurl(self):
        """
            Método encargado de llamar al método cargarInfo en un
             hilo distinto
         """
        self.vista.button.config(state=DISABLED)
        self.vista.bvideo.config(state=DISABLED)
        self.vista.baudio.config(state=DISABLED)
        self.vista.bborrar.config(state=DISABLED)
        if platform.system() == 'Windows':
            self.vista.button.config(cursor="wait")
        t = threading.Thread(target=self.cargarInfo)
        t.start()

    def cargarInfo(self):
        """ Método encargado de obtener información dela url ingresada """
        try:
            self.recurso = pafy.new(self.vista.url.get())
            info = ""
            info += "■Título: " + self.recurso.title+"\n"
            info += "■Duración: " + self.recurso.duration+"\n"
            info += "■Autor: " + self.recurso.author+"\n"
            info += "■Categoría: " + self.recurso.category+"\n"
            info += "■Likes: " + str(self.recurso.likes)+"\n"
            info += "■Dislikes: " + str(self.recurso.dislikes)+"\n"
            mejor = self.recurso.getbest()
            info += "■Mejor resolución: " + mejor.resolution+"\n"
            info += "■Mejor formato: " + mejor.extension
            if self.recurso.bigthumb != '':
                response = requests.get(self.recurso.bigthumb)
                img_data = response.content
                img = ImageTk.PhotoImage(opp(BytesIO(img_data)))
                self.vista.imagen.config(text="", image=img)
                self.vista.imagen.image = img

            self.vista.text.config(state=NORMAL)
            self.vista.text.delete(1.0, END)
            self.vista.text.insert(INSERT, info)
            self.vista.text.config(state=DISABLED)
            self.cargarLista()

        except Exception as e:
            mensaje = "La url es inválida o no se encuentra conectado "
            mensaje += "a internet, intentelo nuevamente."
            msg.showerror("Error", mensaje)

        self.vista.button.config(state=NORMAL)
        self.vista.bvideo.config(state=NORMAL)
        self.vista.baudio.config(state=NORMAL)
        self.vista.bborrar.config(state=NORMAL)
        self.vista.button.config(cursor="")

    def cargarLista(self):
        """
            Método encargado de obtener los formatos disponibles del
            video que se busca
        """

        self.streams = self.recurso.streams
        self.vista.listbox.delete(0, END)
        i = 0
        texto_a_insertar = "{}) Resolución: {}, Extensión: {}, Tamaño: {}"
        for s in self.streams:
            i += 1
            tamanio = str("%.2f MB." % (s.get_filesize()/(1024**2)))
            self.vista.listbox.insert(END, texto_a_insertar.format(
                i, s.resolution, s.extension, tamanio))

    def descargaVideo(self):
        """
            Método encargado de llamar al método __descargaVideo, 
            según lo seleccionado por el usuario además que
            se ejecuta en un hilo distinto    
        """
        index = self.vista.listbox.curselection()
        if len(index) > 0:
            self.seleccion = self.streams[index[0]]
            self.size = self.seleccion.get_filesize()

            t = threading.Thread(target=self.__descargarVideo)
            t.start()

            self.vista.button.config(state=DISABLED)
            self.vista.bvideo.config(state=DISABLED)
            self.vista.baudio.config(state=DISABLED)
            self.mostrarDialogo()
        else:
            msg.showerror("Error", "Se debe seleccionar un video de la lista.")

    def __descargarVideo(self):
        """ Método que descarga el video seleccionado y muestra la carga """
        self.d = True
        try:
            file = self.seleccion.download(
                quiet=True, filepath=self.vista.path.get(),
                callback=self.callback)

        except Exception as e:
            raise e
            msg.showerror("Error", "El archivo ya existe.")

        self.top.destroy()
        self.d = False
        msg.showinfo("Mensaje", "Archivo descargado correctamente")
        self.vista.text.config(state=NORMAL)
        self.vista.text.delete(1.0, END)
        self.vista.text.config(state=DISABLED)
        self.vista.listbox.delete(0, END)
        self.vista.url.set("")
        self.vista.imagen.config(text="No disponible", image='')
        self.vista.imagen.image = ''
        self.vista.button.config(state=NORMAL)
        self.vista.bvideo.config(state=NORMAL)
        self.vista.baudio.config(state=NORMAL)

    def descargaAudio(self):
        """
            Método encargado de llamar al método __descargaAudio, 
            que descarga la mejor resolución de audio, además que
            se ejecuta en un hilo distinto    
        """
        if self.recurso != None:
            t = threading.Thread(target=self.__descargaAudio)
            t.start()
            self.vista.button.config(state=DISABLED)
            self.vista.bvideo.config(state=DISABLED)
            self.vista.baudio.config(state=DISABLED)
            self.mostrarDialogo()

    def __descargaAudio(self):
        """ Método que descarga el video seleccionado y muestra la carga """
        self.bestaudio = self.recurso.getbestaudio(preftype='m4a')
        if self.bestaudio != None:
            self.d = True
            self.fileaudio = self.bestaudio.title+".m4a"
            self.size = self.bestaudio.get_filesize()
            try:
                self.bestaudio.download(
                    quiet=True, callback=self.callback,
                    filepath=self.vista.path.get())

                msg.showinfo("Mensaje", "Archivo descargado correctamente.")

            except Exception as e:
                msg.showerror("Error", "El archivo ya existe.")

        self.top.destroy()
        self.d = False
        self.vista.text.config(state=NORMAL)
        self.vista.text.delete(1.0, END)
        self.vista.text.config(state=DISABLED)
        self.vista.listbox.delete(0, END)
        self.vista.url.set("")
        self.vista.imagen.config(text="No disponible", image='')
        self.vista.imagen.image = ''
        self.vista.button.config(state=NORMAL)
        self.vista.bvideo.config(state=NORMAL)
        self.vista.baudio.config(state=NORMAL)

    def mostrarDialogo(self):
        """ Método que muestra la GUI de descarga del archivo """
        self.top = Toplevel(self.vista)
        self.top.resizable(0, 0)
        geometry = "400x100+"
        geometry += str(int(self.vista.ancho/2)-150)+"+"
        geometry += str(int(self.vista.alto/2)-50)
        self.top.geometry(geometry)
        self.top.title("Descarga en progreso...")
        self.label = Label(self.top, text="Descargando: ", font=("Arial", 13))
        self.label.place(x=5, y=15)
        self.label2 = Label(self.top, text="Tiempo: ", font=("Arial", 13))
        self.label2.place(x=140, y=15)
        self.label3 = Label(self.top, text="Vel.: ", font=("Arial", 13))
        self.label3.place(x=260, y=15)
        self.progress = IntVar()
        self.progress.set(0)
        self.progressbar = ttk.Progressbar(self.top, variable=self.progress)
        self.progressbar.place(x=30, y=60, width=320)
        if platform.system() == 'Windows':
            self.vista.button.config(cursor="wait")
        self.top.transient(self.vista)

    def iniciar(self):
        """ Método que muestra la GUI """
        self.vista.mainloop()

    def borrarurl(self):
        """ Método borra la url ingresada """
        self.vista.url.set("")

    def callback(self, total, recvd, ratio, rate, eta):
        """ Método que controla la descarga del archivo """
        carga = int(ratio*100)
        self.progressbar.step(carga - self.progress.get())
        self.progress.set(carga)
        self.label.config(text="Descarga: "+str(carga)+" %")
        self.label2.config(text="Tiempo: "+str("%.0f" % (eta))+" sec")
        self.label3.config(text="Vel.: "+str("%.2f" % (rate))+" kbps")

    def cambiaPath(self):
        """ Método para cambiar la carpeta destino """
        path = filedialog.askdirectory()
        if path != None and path != '':
            self.vista.path.set(path)

    def copia(self, event):
        """ Método que pega la url del portapapeles """
        self.vista.url.set(self.vista.clipboard_get())
