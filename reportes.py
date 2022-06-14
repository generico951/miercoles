from tkinter import *
from matplotlib.pyplot import text
from controlador.manipular_datos import *
import tkinter
from PIL import ImageTk,Image
import tkinter.messagebox
import customtkinter
from controlador.ver_camaras_conectadas import *
from controlador.manipular_reportes import *

class ventana_reportes():

    def __init__(self):
        self.ventana=customtkinter.CTk()
        self.ventana.geometry("500x700")
        self.titulo=customtkinter.CTkLabel(self.ventana,text="Reportes")
        self.titulo.grid(column=0,row=0)
        self.cargar_reportes()
        self.ventana.mainloop()


    def cargar_reportes(self):
        self.frame_reportes=customtkinter.CTkFrame(self.ventana)
        self.reportes= obtener_reportes()
        i=1
        for reporte in self.reportes:
            texto=""
            texto+="Camara: "+self.reportes[reporte]["camara"]
            texto+="\n Ubicacion: "+self.reportes[reporte]["ubicacion"]
            texto+="\n Fecha y hora: "+self.reportes[reporte]["fecha_hora"]            
            texto+="\n Deteccion: "+self.reportes[reporte]["objetos"]
            texto+="\n Ruta de la imagen:"+"./registros/imagenes/"+self.reportes[reporte]["id_imagen"]
            texto+="\n"
            self.cargar_reporte(contenido=texto,fila=i, 
                                ruta_imagen="./registros/imagenes/"+self.reportes[reporte]["id_imagen"],
                                id_reporte=reporte)
            i+=1
        self.frame_reportes.grid(column=0,row=1)


    def cargar_reporte(self,contenido,fila,ruta_imagen,id_reporte):
        frameReporte=customtkinter.CTkFrame(self.frame_reportes)
        labelReporte=customtkinter.CTkLabel(frameReporte,text=contenido)
        
        imagen_reporte=ImageTk.PhotoImage(Image.open(ruta_imagen).resize((200,200)))
        label_imagen_reporte=Label(frameReporte,text=ruta_imagen,bg="#E6DAD7")


        boton_borrar_reporte = customtkinter.CTkButton(master=frameReporte,
                                                        text="Descartar reporte",
                                                        command=lambda: self.descartar_reporte(id_reporte),
                                                        fg_color=("red", "red")
                                                        )


        boton_borrar_reporte.grid(column=1,row=1)
        labelReporte.grid(column=0,row=0)
        label_imagen_reporte.grid(column=1,row=0)
        frameReporte.grid(column=0,row=fila)

    def descartar_reporte(self,id_reporte):
        eliminar_reporte(id_reporte)
        self.frame_reportes.destroy()
        self.cargar_reportes()





