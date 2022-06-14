import cv2
def obtener_camaras_conecatadas():
    lista_camaras=[]
    cam_1=cv2.VideoCapture(0)
    cam_2=cv2.VideoCapture(1)
    cam_3=cv2.VideoCapture(2)
    cam_4=cv2.VideoCapture(3)
    
    try:
        cam_1_conectada,im1=cam_1.read()
    except: 
        pass
    try:
        cam_2_conectada,im2=cam_2.read()
    except: 
        pass
    try:
        cam_3_conectada,im3=cam_3.read()
    except: 
        pass
    try:
        cam_4_conectada,im4=cam_4.read()
    except: 
        pass
    
    if(cam_1_conectada):
        lista_camaras.append("camara_1")
    if(cam_2_conectada):
        lista_camaras.append("camara_2")
    if(cam_3_conectada):
        lista_camaras.append("camara_3")
    if(cam_4_conectada):    
        lista_camaras.append("camara_4")



    return(lista_camaras)
