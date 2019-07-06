
#__author__=jjr4p
#Vista descarga video y audio de youtube con python

import os
try:
	import pafy
except Exception as e:
	os.system("pip install pafy && pip install youtube-dl")
	import pafy

try:
	from tkinter import *
	from tkinter import messagebox as msg
	from tkinter import ttk
	from tkinter import filedialog

except Exception as e:
	os.system("pip install tkinter")
	from tkinter import *
	from tkinter import messagebox as msg
	from tkinter import ttk
	from tkinter import filedialog

import ctypes
import threading
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class Downloader(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, *kwargs)
		self.recurso = None
		self.geometry("410x600+"+str(int(ancho/2)-205)+"+"+str(int(alto/2)-300))
		self.resizable(0,0)
		self.title("Downloader")
		self.url = StringVar()
		Label(self, text="Downloader youtube", font=("Tahoma",25), fg="#EE0000").place(x=50,y=5)
		Label(self, text="URL:", font=("Tahoma",14)).place(x=10, y=60)
		Entry(self, textvariable=self.url, width=28, font=("Tahoma",12)).place(x=65,y=64)
		self.button = Button(self, text="Cargar url", font=("Tahoma",11), command=self.cargarurl)
		self.button.place(x=325,y=60)
		Label(self, text="Info de la url:", font=("Tahoma",13)).place(x=10, y=110)
		self.text = Text(self, width=43, height=9, font=("Tahoma",12))
		self.text.config(state=DISABLED)
		self.text.place(x=10,y=140)
		Label(self, text="Disponibles: ", font=("Tahoma",13)).place(x=10, y=320)
		scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
		self.listbox = Listbox(self,height=5, width=35 ,font=("Tahoma",13), yscrollcommand=scrollbar.set)
		self.listbox.config(selectforeground="#ffffff",
                                  selectbackground="#00aa00",
                                  selectborderwidth=1)
		self.listbox.place(x=30,y=350)
		self.bvideo = Button(self, text="Descargar video", font=("Tahoma",14), command=self.descargaVideo)
		self.bvideo.place(x=40, y=500)
		self.baudio = Button(self, text="Descargar audio", font=("Tahoma",14), command=self.descargaAudio)
		self.baudio .place(x=220, y=500)

	def cargarurl(self):
		self.button.config(state=DISABLED)
		self.bvideo.config(state=DISABLED)
		self.baudio.config(state=DISABLED)
		self.button.config(cursor="wait")
		t = threading.Thread(target=self.cargarInfo)
		t.start()

	def cargarInfo(self):
		try:
			self.recurso = pafy.new(self.url.get())
			info = ""
			info += "■Título: " + self.recurso.title+"\n"
			info += "■Duración: " + self.recurso.duration+"\n"
			info += "■Autor: " + self.recurso.author+"\n"
			info += "■Categoría: " + self.recurso.category+"\n"
			info += "■Likes: " + str(self.recurso.likes)+"\n"
			info += "■Dislikes: " + str(self.recurso.dislikes)+"\n"
			mejor = self.recurso.getbest()
			info += "■Mejor resolución: " + mejor.resolution+"\n"
			info += "■Mejor formato: " + mejor.extension+"\n"
			self.text.config(state=NORMAL)
			self.text.delete(1.0,END)
			self.text.insert(INSERT, info)
			self.text.config(state=DISABLED)
			self.cargarLista()

		except ValueError as e:
			msg.showerror("Error","La url es inválida, intentelo nuevamente.")

		self.button.config(state=NORMAL)
		self.bvideo.config(state=NORMAL)
		self.baudio.config(state=NORMAL)
		self.button.config(cursor="")

	def cargarLista(self):
		self.streams = self.recurso.streams
		self.listbox.delete(0,END)
		i = 1
		for s in self.streams:
			self.listbox.insert(END,str(i)+") Resolución: "+s.resolution+", Extensión: "+s.extension)
			i += 1

	def descargaVideo(self):
		index = self.listbox.curselection()
		if len(index) > 0:
			self.seleccion = self.streams[index[0]]
			self.path = filedialog.askdirectory()
			self.size = self.seleccion.get_filesize()

			t = threading.Thread(target= self.__descargarVideo)
			t.start()

			self.button.config(state=DISABLED)
			self.bvideo.config(state=DISABLED)
			self.baudio.config(state=DISABLED)
			self.mostrarDialogo()
			
			t = threading.Thread(target= self.__mostrarCarga)
			t.start()
		else:
			msg.showerror("Error","Se debe seleccionar un video de la lista.")					

	def __descargarVideo(self):
		self.d = True
		try:
			file = self.seleccion.download(quiet=True, filepath=self.path)
		except FileExistsError as e:
			msg.showerror("Error","El archivo ya existe.")

		self.top.destroy()
		self.d = False
		msg.showinfo("Mensaje","Archivo descargado correctamente")
		self.text.config(state=NORMAL)
		self.text.delete(1.0,END)
		self.text.config(state=DISABLED)
		self.listbox.delete(0,END)
		self.url.set("")
		self.button.config(state=NORMAL)
		self.bvideo.config(state=NORMAL)
		self.baudio.config(state=NORMAL)

	def __mostrarCarga(self):
		import os
		while self.d:
			try:
				sizefile = os.stat(str(self.path+"/"+self.seleccion.title+"."+self.seleccion.extension+".temp")).st_size
				carga = int(sizefile/self.size*100)
				self.progressbar.step(carga - self.progress.get())
				self.progress.set(carga)
				self.label.config(text="Descargando: "+str(carga)+" %")
			except FileNotFoundError as e:
				pass

	def __mostrarCargaAudio(self):
		import os
		while self.d:
			try:
				sizefile = os.stat(str(self.fileaudio+".temp")).st_size
				carga = int(sizefile/self.size*100)
				self.progressbar.step(carga - self.progress.get())
				self.progress.set(carga)
				self.label.config(text="Descargando: "+str(carga)+" %")
			except FileNotFoundError as e:
				pass

	def descargaAudio(self):
		if self.recurso != None:
			self.path = filedialog.askdirectory()
			t = threading.Thread(target= self.__descargaAudio)
			t.start()
			self.button.config(state=DISABLED)
			self.bvideo.config(state=DISABLED)
			self.baudio.config(state=DISABLED)
			self.mostrarDialogo()
			t = threading.Thread(target= self.__mostrarCargaAudio)
			t.start()

	def __descargaAudio(self):
		
		self.bestaudio = self.recurso.getbestaudio(preftype='m4a')
		if self.bestaudio != None:
			self.d = True
			self.fileaudio = self.bestaudio.title+".m4a"
			self.size = self.bestaudio.get_filesize()
			try:
				self.bestaudio.download(quiet=True)
				comando = "move \"" + self.fileaudio +"\" "+ self.path
				os.system(comando+" > null && del null")
				msg.showinfo("Mensaje","Archivo descargado correctamente.")
				
			except FileExistsError as e:
				msg.showerror("Error","El archivo ya existe.")

			self.top.destroy()
			self.text.config(state=NORMAL)
			self.text.delete(1.0,END)
			self.text.config(state=DISABLED)
			self.listbox.delete(0,END)
			self.url.set("")
			self.button.config(state=NORMAL)
			self.bvideo.config(state=NORMAL)
			self.baudio.config(state=NORMAL)

	def mostrarDialogo(self):
		self.top = Toplevel(self)
		self.top.resizable(0,0)
		self.top.geometry("300x100+"+str(int(ancho/2)-150)+"+"+str(int(alto/2)-50))
		self.top.title("Descarga en progreso...")
		self.label = Label(self.top, text = "Descargando: ", font=("Tahoma",13))
		self.label.place(x=5,y=15)
		self.progress = IntVar()
		self.progress.set(0)
		self.progressbar = ttk.Progressbar(self.top, variable=self.progress)
		self.progressbar.place(x=30, y=60, width=220)
		self.top.config(cursor="wait")
		self.top.transient(self)

r = Downloader()
r.mainloop()



