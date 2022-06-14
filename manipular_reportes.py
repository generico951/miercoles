import json

def obtener_reportes():
    archivo=open("./registros/reportes.json","r")
    reportes=json.loads(archivo.read())
    archivo.close()
    return reportes

def agregar_reporte(camara,ubicacion,fecha_hora,objetos,id_imagen):
    reporte={camara+fecha_hora:{
        "camara":camara,
        "ubicacion":ubicacion,
        "fecha_hora":fecha_hora,
        "objetos":objetos,
        "id_imagen":id_imagen
    }}
    archivo_lectura=open("./registros/reportes.json","r")
    reportes=json.loads(archivo_lectura.read())
    string_reporte=json.dumps (reporte,indent=4)
    string_reportes=json.dumps(reportes,indent=4)
    archivo_lectura.close()

    archivo_escritura=open("./registros/reportes.json","w")
    if(string_reportes=="{}" or string_reportes=="" or string_reportes==" "):
        archivo_escritura.write(string_reporte[0:len(string_reporte)])
    else:
        union=string_reportes[0:len(string_reportes)-1]+","+string_reporte[1:len(string_reporte)]
        archivo_escritura.write(union)
    archivo_escritura.close()

def eliminar_reporte(reporte):
    try:
        archivo_lectura=open("./registros/reportes.json","r")
        reportes=json.loads(archivo_lectura.read())
        archivo_lectura.close()
        del reportes[reporte]

        archivo_escritura=open("./registros/reportes.json","w")
        archivo_escritura.write(json.dumps(reportes))
        archivo_escritura.close()
    except:
        pass



