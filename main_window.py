import cv2
import numpy as np
from tkinter import *
from PIL import ImageTk,Image
import imutils
import logging
import threading
import time
import datetime
from ventana_gestionar_camaras import ventana_gestionar_camaras
from manipular_datos import leer_estado_camaras

class ventana_inicio:
    def __init__(self):
        self.captura=None
        self.ventana=None
        self.frameBotones=None
        self.frameCamaras=None
        self.botonGestionCamaras=None
        self.imagen1=None
        self.camara1=None
        self.inice_antes=False
        self.archivo_js=None
       
    def pintar(self):
        self.ventana=Tk()
        self.ventana.title("video vigilancia inteligente")
        self.ventana.geometry("1200x635")
        self.ventana.config(bg="#231F1F",padx=20)

        self.frameBotones=Frame(self.ventana)
        self.frameCamaras=Frame(self.ventana)
        self.frameBotones.config(bg="#293462") 
  
        self.frameCamaras.config(bg="#544C4C")
        self.frameBotones.config(width=480,height=500)
        self.frameCamaras.config(width=1000,height=610)

    
        self.botonGestionCamaras=Button(self.frameBotones,text="Administrar camaras",command=ventana_gestionar_camaras,bg="#3F72C4",font="Poppins")
        self.imagen1=ImageTk.PhotoImage(Image.open('./assets/camera_unconnect.png').resize((200,200)))
        self.camara1=Label(self.frameCamaras,image=self.imagen1,bg="black")
        self.frameBotones.grid(row=0,column=0)
        self.botonGestionCamaras.grid(row=0,column=0)
        self.frameCamaras.grid(row=0,column=2, pady=20)
        
        
        if(self.archivo_js["camara_1"]["estado"]=="conectado"):
            self.captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)
            self.visualizar()

        self.ventana.mainloop()
        #self.recuperar_estado_camaras()
        

    # def recuperar_estado_camaras(self):
    #     self.archivo_js=leer_estado_camaras()
    #     if(self.archivo_js["camara_1"]["estado"]=="conectado"):
    #         self.iniciar(0)



    def visualizar(self):
        if self.captura is not None:
            ret,frame=self.captura.read()
            if ret ==True:
                ##               
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
        while True:
            self.archivo_js=leer_estado_camaras()
            if (self.archivo_js["camara_1"]["estado"]=="conectado"):
                if not(self.inice_antes):
                    self.inice_antes=True
                    self.captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)
                    self.visualizar()
            else:
                if(self.captura!=None):
                    self.captura.release()
                    self.inice_antes=False
                    self.imagen1=ImageTk.PhotoImage(Image.open('./assets/camera_unconnect.png').resize((200,200)))
                    self.camara1.config(image=self.imagen1)

                print("noo")
            time.sleep(0.1)
            
def hilos():
    ventana_principal=ventana_inicio()
    canal_1=threading.Thread(name="ventana_principal",target=ventana_principal.pintar,args=())
    canal_2=threading.Thread(name="contador",target=ventana_principal.cargar_estado_camaras,args=())    
    canal_1.start()
    canal_2.start()

    canal_1.join()
    canal_2.join()

hilos()



        
        # capCamera = cv2.VideoCapture(0)
# capVideo  = cv2.VideoCapture("C:/Users/Mirco/Documents/proyecto de grado/vista/minecraft.mp4")

# while True:
#     exitoCamara, imagenCamara = capCamera.read()
#     exitoVideo, imagenVideo = capVideo.read()


#     final = cv2.hconcat([imagenCamara,imagenCamara])
#     cv2.imshow("fina",final)

#     if cv2.waitKey(1) & 0xFF==ord('q'):
#      break

# capCamera.release()
# capVideo.release()
# cv2.destroyAllWindows()

