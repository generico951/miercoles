from tkinter import *
from vista.ventana_registro import ventana_registro_camara
from controlador.manipular_datos import *
import tkinter
import tkinter.messagebox
from turtle import width
import customtkinter
from controlador.ver_camaras_conectadas import *
class ventana_gestionar_camaras():

    def __init__(self):
        self.ventana=customtkinter.CTk()
        self.ventana.geometry("300x300")
        self.titulo=Label(self.ventana,text="Gestionar cámara")
        self.lista_camaras=obtener_camaras_conecatadas()
        self.frameCamaras=LabelFrame(self.ventana)
        self.frameCamaras.config(width=600,height=450,bg="#A9A8A8")
        self.titulo.grid(row=0,column=2)
        self.frameCamaras.grid(row=2,column=2)

        self.iniciar_componentes()
        self.ventana.mainloop()


    def cerrar_editor(self):
        self.campoNombre1.destroy()
        self.menu1.destroy()
        self.botonAceptarCambios1.destroy()
        self.botonCancelarEditar1.destroy()
        self.iniciar_componentes()

    def abrir_editor(self):
        self.nombre1.destroy()
        self.modelo1.destroy()
        self.estado1.destroy()
        self.botonEditar1.destroy()
        self.botonBorrar1.destroy()

        self.campoNombre1.grid(row=2,column=0)
        self.menu1.grid(row=4,column=0)
        self.botonAceptarCambios1.grid(row=5,column=0)
        self.botonCancelarEditar1.grid(row=5,column=1)

    def eliminar_camara(self):
        self.nombre1.destroy()
        self.modelo1.destroy()
        self.estado1.destroy()
        self.botonEditar1.destroy()
        self.botonBorrar1.destroy()
        desactivar_camara("camara_1")
        self.iniciar_componentes()

    def actualizar_ventana(self):
        nombre=self.campoNombre1.get()
        modelo=self.opcionSeleccionada.get()
        activar_camara(nombre=nombre,modelo=modelo,camara="camara_1")
        self.cerrar_editor()

    def iniciar_componentes(self):
        self.datos_js=leer_estado_camaras()

        self.nombre1=customtkinter.CTkLabel(master=self.frameCamaras,text=self.datos_js["camara_1"]["nombre"])
        self.estado1=customtkinter.CTkLabel(master=self.frameCamaras,text=self.datos_js["camara_1"]["estado"])
        self.modelo1=customtkinter.CTkLabel(master=self.frameCamaras,text=self.datos_js["camara_1"]["modelo"])

        self.campoNombre1=customtkinter.CTkEntry(self.frameCamaras)

        self.opcionSeleccionada = StringVar(self.frameCamaras)
        
        self.opcionSeleccionada.set(self.lista_camaras[0])
        
        self.menu1 = OptionMenu(self.frameCamaras, self.opcionSeleccionada,*self.lista_camaras) 

        self.botonEditar1=customtkinter.CTkButton(self.frameCamaras,text="Editar",command=self.abrir_editor,fg_color=("#5AF06C", "#5AF06C"))
        self.botonBorrar1=customtkinter.CTkButton(self.frameCamaras,text="Eliminar",command=self.eliminar_camara,fg_color=("red", "red"))

        self.botonAceptarCambios1=customtkinter.CTkButton(self.frameCamaras,text="Aceptar Cambios",command=self.actualizar_ventana,fg_color=("#5AF06C", "#5AF06C"))
        self.botonCancelarEditar1=customtkinter.CTkButton(self.frameCamaras,text="Cancelar",command=self.cerrar_editor,fg_color=("red", "red"))
        
        self.nombre1.grid(row=2,column=0)
        self.estado1.grid(row=3,column=0)
        self.modelo1.grid(row=4,column=0)
        self.botonEditar1.grid(row=5,column=0)
        self.botonBorrar1.grid(row=5,column=1)


    





