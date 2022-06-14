import json

def leer_estado_camaras():
    archivo=open("./registros/estado_camaras.json","r")
    camaras_js=json.loads(archivo.read())
    archivo.close()
    return camaras_js

def guardar_estado_camaras(archivo_js):
    archivo=open("./registros/estado_camaras.json","w")
    camaras_js=json.dumps(archivo_js,indent=4)
    archivo.write(camaras_js)
    archivo.close()
    return camaras_js

def leer_camara(camara):
    return leer_estado_camaras()[camara]


def desactivar_camara(camara):
    archivo_js=leer_estado_camaras()
    if( archivo_js[camara]["estado"]=="conectado"):
        archivo_js[camara]["nombre"]=""
        archivo_js[camara]["modelo"]=""
        archivo_js[camara]["estado"]="desconectado"
    guardar_estado_camaras(archivo_js)


def activar_camara(nombre,modelo,camara):
    archivo_js=leer_estado_camaras()
    if(archivo_js[camara]["estado"]=="desconectado"):
        archivo_js[camara]["nombre"]=nombre
        archivo_js[camara]["modelo"]=modelo
        archivo_js[camara]["estado"]="conectado"

    guardar_estado_camaras(archivo_js)


