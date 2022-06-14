from tkinter import *
import tkinter.messagebox
from turtle import width
import customtkinter
import cv2
import numpy as np
from PIL import ImageTk,Image
import imutils
import threading
import time
from vista.ventana_gestionar_camaras import ventana_gestionar_camaras
from vista.reportes import ventana_reportes
from controlador.manipular_datos import leer_estado_camaras
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")  

class ventana_principal(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.captura=None
        self.ventana=None
        self.frameBotones=None
        self.frameCamaras=None
        self.botonGestionCamaras=None
        self.imagen1=None
        self.camara1=None
        self.inice_antes=False
        self.archivo_js=None
        self.boton_reportes=None
        self.hilo1=None
        self.detener_cargar_estado=False
        self.pintar()

    def pintar(self):
        self.title("Deteccion de conducta criminal UMSS")
        self.geometry(f"{ventana_principal.WIDTH}x{ventana_principal.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    #=====================frame derecho y frame de las camaras====================================#
        self.frameBotones = customtkinter.CTkFrame(master=self,width=180,corner_radius=0)
        self.frameBotones.grid(row=0, column=0, sticky="nswe")

        self.frameCamaras=customtkinter.CTkFrame(master=self,width=ventana_principal.WIDTH/2,height=ventana_principal.WIDTH/2)
        self.frameCamaras.grid(row=0, column=1)

        self.frameBotones.grid_rowconfigure(0, minsize=10) 
        self.frameBotones.grid_rowconfigure(5, weight=1) 
        self.frameBotones.grid_rowconfigure(8, minsize=20)   
        self.frameBotones.grid_rowconfigure(11, minsize=10)  
    #=============================================================================================#

    #=====================label de opciones====================================#
        self.label_1 = customtkinter.CTkLabel(master=self.frameBotones, text="Opciones", text_font=("Roboto Medium", -16)) 
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
    #===========================================================================#

    #=====================botones del frame de opciones izquierdo====================================#
        self.botonGestionCamaras = customtkinter.CTkButton(master=self.frameBotones,text="Gestionar cámaras",
                                                                 fg_color=("gray75", "gray30"),  
                                                                 command=ventana_gestionar_camaras)
        self.botonGestionCamaras.grid(row=2, column=0, pady=10, padx=20)

        self.boton_reportes = customtkinter.CTkButton(master=self.frameBotones,
                                                text="Revisar reportes",
                                                fg_color=("gray75", "gray30"),
                                                command=ventana_reportes)

        self.boton_reportes.grid(row=3, column=0, pady=10, padx=20)


        self.switch_2 = customtkinter.CTkSwitch(master=self.frameBotones,
                                                text="Modo nocturno",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")
        self.switch_2.select()
    #====================================================================================================#

    #===========================frame derecho de la camara=================================#
        self.camara1=Label(self.frameCamaras,bg="black")
    def loop(self):
        self.mainloop()

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.detener_cargar_estado=True
        self.destroy()
    
    def visualizar(self):
        if self.captura is not None:
            ret,frame=self.captura.read()
            if ret ==True:              
                frame=imutils.resize(frame,width=500)
                frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

             
                im=Image.fromarray(frame)
                img=ImageTk.PhotoImage(image=im)
                self.camara1.configure(image=img)
                self.camara1.image=img
                self.camara1.after(10,self.visualizar)
            else:
                self.camara1.image=""
                self.captura.release()
        else:
            self.camara1.image=""
            self.captura.release()
        
    def cargar_estado_camaras(self):
        time.sleep(2)
        while True:
            self.archivo_js=leer_estado_camaras()
            if (self.archivo_js["camara_1"]["estado"]=="conectado"):
                if not(self.inice_antes):
                    self.camara1.grid(row=0,column=0)
                    self.inice_antes=True
                    self.captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)
                    self.visualizar()
            else:
                if(self.captura!=None):
                    self.captura.release()
                    self.inice_antes=False
            if self.detener_cargar_estado:
                break
            
            time.sleep(2)

if __name__ == "__main__":
    ventana_principal=ventana_principal()
    ventana_principal.pintar()


