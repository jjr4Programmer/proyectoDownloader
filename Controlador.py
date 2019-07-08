
import platform
import threading
from io import BytesIO
import os
import requests


try:
	from PIL import ImageTk
	from PIL.Image import open as opp
except:
	if platform.system() == 'Windows':
		os.system("pip install Pillow")
	elif platform.system() == 'Linux':
		os.system("sudo pip3 install Pillow")
	from PIL import ImageTk, Image

try:
	import pafy
except Exception as e:
	if platform.system() == 'Windows':
		os.system("pip install pafy && pip install youtube-dl")
	elif platform.system() == 'Linux':
		os.system("sudo pip3 install youtube-dl && sudo apt-get install python3-pafy")
	import pafy

try:
	from tkinter import *
	from tkinter import messagebox as msg
	from tkinter import ttk
	from tkinter import filedialog

except Exception as e:
	if platform.system() == 'Windows':
		os.system("pip install tkinter")
	elif platform.system() == 'Linux':
		os.system("sudo pip3 install tkinter")	
	from tkinter import *
	from tkinter import messagebox as msg
	from tkinter import ttk
	from tkinter import filedialog

class Controlador:

	def __init__(self):
		pass
	
	def setVista(self, vista):
		self.vista = vista

	def cargarurl(self):
		self.vista.button.config(state=DISABLED)
		self.vista.bvideo.config(state=DISABLED)
		self.vista.baudio.config(state=DISABLED)
		self.vista.bborrar.config(state=DISABLED)
		if platform.system() == 'Windows':
			self.vista.button.config(cursor="wait")
		t = threading.Thread(target=self.cargarInfo)
		t.start()

	def cargarInfo(self):
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
				self.vista.imagen.config(text="",image = img)
				self.vista.imagen.image = img

			self.vista.text.config(state=NORMAL)
			self.vista.text.delete(1.0,END)
			self.vista.text.insert(INSERT, info)
			self.vista.text.config(state=DISABLED)
			self.cargarLista()

		except Exception as e:
			msg.showerror("Error","La url es inválida o no se encuentra conectado a internet, intentelo nuevamente.")

		self.vista.button.config(state=NORMAL)
		self.vista.bvideo.config(state=NORMAL)
		self.vista.baudio.config(state=NORMAL)
		self.vista.bborrar.config(state=NORMAL)
		self.vista.button.config(cursor="")

	def cargarLista(self):
		self.streams = self.recurso.streams
		self.vista.listbox.delete(0,END)
		i = 1
		for s in self.streams:
			self.vista.listbox.insert(END,str(i)+") Resolución: "+s.resolution+", Extensión: "+s.extension+", Tamaño: "+str("%.2f MB." % (s.get_filesize()/(1024**2))))
			i += 1

	def descargaVideo(self):
		index = self.vista.listbox.curselection()
		if len(index) > 0:
			self.seleccion = self.streams[index[0]]
			self.path = filedialog.askdirectory()
			self.size = self.seleccion.get_filesize()

			t = threading.Thread(target= self.__descargarVideo)
			t.start()

			self.vista.button.config(state=DISABLED)
			self.vista.bvideo.config(state=DISABLED)
			self.vista.baudio.config(state=DISABLED)
			self.mostrarDialogo()
			
			t = threading.Thread(target= self.__mostrarCarga)
			t.start()
		else:
			msg.showerror("Error","Se debe seleccionar un video de la lista.")					

	def __descargarVideo(self):
		self.d = True
		try:
			file = self.seleccion.download(quiet=True, filepath=self.path)
		except:
			msg.showerror("Error","El archivo ya existe.")

		self.top.destroy()
		self.d = False
		msg.showinfo("Mensaje","Archivo descargado correctamente")
		self.vista.text.config(state=NORMAL)
		self.vista.text.delete(1.0,END)
		self.vista.text.config(state=DISABLED)
		self.vista.listbox.delete(0,END)
		self.vista.url.set("")
		self.vista.imagen.image=None
		self.vista.imagen.config(text="No disponible", image=None)
		self.vista.button.config(state=NORMAL)
		self.vista.bvideo.config(state=NORMAL)
		self.vista.baudio.config(state=NORMAL)

	def __mostrarCarga(self):
		import os
		while self.d:
			try:
				sizefile = os.stat(str(self.path+"/"+self.seleccion.title+"."+self.seleccion.extension+".temp")).st_size
				carga = int(sizefile/self.size*100)
				self.progressbar.step(carga - self.progress.get())
				self.progress.set(carga)
				self.label.config(text="Descargando: "+str(carga)+" %")
			except:
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
			except:
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
				if platform.system() == 'Windows':
					comando = "move \"" + self.fileaudio +"\" "+ self.path
					os.system(comando+" > null && del null")
				elif platform.system() == 'Linux':
					comando = "mv \"" + self.fileaudio +"\" "+ self.path
					os.system(comando+" > null && rm null")
				msg.showinfo("Mensaje","Archivo descargado correctamente.")
				
			except:
				msg.showerror("Error","El archivo ya existe.")

			self.top.destroy()
			self.vista.deiconify()
			self.text.config(state=NORMAL)
			self.text.delete(1.0,END)
			self.text.config(state=DISABLED)
			self.listbox.delete(0,END)
			self.url.set("")
			self.button.config(state=NORMAL)
			self.bvideo.config(state=NORMAL)
			self.baudio.config(state=NORMAL)

	def mostrarDialogo(self):
		self.top = Toplevel(self.vista)
		self.top.resizable(0,0)
		self.top.geometry("300x100+"+str(int(self.vista.ancho/2)-150)+"+"+str(int(self.vista.alto/2)-50))
		self.top.title("Descarga en progreso...")
		self.label = Label(self.top, text = "Descargando: ", font=("Arial",13))
		self.label.place(x=5,y=15)
		self.progress = IntVar()
		self.progress.set(0)
		self.progressbar = ttk.Progressbar(self.top, variable=self.progress)
		self.progressbar.place(x=30, y=60, width=220)
		if platform.system() == 'Windows':
			self.vista.button.config(cursor="wait")
		self.top.transient(self.vista)

	def iniciar(self):
		self.vista.mainloop()

	def borrarurl(self):
		self.vista.url.set("")



