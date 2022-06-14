import argparse
from datetime import datetime
import os
import sys
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn
import threading
from controlador.manipular_datos import leer_estado_camaras
from controlador.manipular_reportes import agregar_reporte

from models.common import DetectMultiBackend
from utils.datasets import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

from vista.ventana_principal import *


hilo1=None
hilo2=None
ventana_inicio=None
detener_procesar_imagen=False
font=cv2.FONT_ITALIC
def procesar_imagen():
    ##leo los pesos entrenados para la camara X
    weights='yolov3.pt'  # model.pt path(s)
    source=0  # file/dir/URL/glob, 0 for webcam
    imgsz=320  # inference size (pixels)
    conf_thres=0.25  # confidence threshold
    iou_thres=0.45  # NMS IOU threshold
    max_det=1000  # maximum detections per image
    device=""   # cuda device, i.e. 0 or 0,1,2,3 or cpu
    view_img=False  # show results
    save_txt=False  # save results to *.txt
    save_conf=False  # save confidences in --save-txt labels
    save_crop=False  # save cropped prediction boxes
    nosave=False  # do not save images/videos
    classes=None  # filter by class: --class 0, or --class 0 2 3
    agnostic_nms=False  # class-agnostic NMS
    augment=False  # augmented inference
    visualize=False  # visualize features
    update=False  # update all models
    project='runs/detect'  # save results to project/name
    name='exp'  # save results to project/name
    exist_ok=False  # existing project/name ok, do not increment
    line_thickness=3  # bounding box thickness (pixels)
    hide_labels=False  # hide labels
    hide_conf=False  # hide confidences
    half=False  # use FP16 half-precision inference
    dnn=False  # use OpenCV DNN for ONNX inference
    
    source = str(0)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn)
    stride, names, pt, jit, onnx = model.stride, model.names, model.pt, model.jit, model.onnx
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Half
    half &= pt and device.type != 'cpu'  # half precision only supported by PyTorch on CUDA
    if pt:
        model.model.half() if half else model.model.float()

    # Dataloader
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt and not jit)
        bs = len(dataset)  # batch_size

    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.model.parameters())))  # warmup
    dt, seen = [0.0, 0.0, 0.0], 0

    prediccion_reciente=""
    hora_ultima_prediccion=""
    for path, im, im0s, vid_cap, s in dataset: 
        time.sleep(1)
        estados_conexion=leer_estado_camaras()
        if (estados_conexion["camara_1"]["estado"]=="conectado"):

            t1 = time_sync()
            im = torch.from_numpy(im).to(device)
            im = im.half() if half else im.float() 
            im /= 255 
            if len(im.shape) == 3:
                im = im[None]  
            t2 = time_sync()
            dt[0] += t2 - t1

          
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)
            t3 = time_sync()
            dt[1] += t3 - t2

            # NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
            dt[2] += time_sync() - t3

            # Process predictions
            for i, det in enumerate(pred):  
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    # s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)


                p = Path(p) 
            
                # s += '%gx%g ' % im.shape[2:]  
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det):
                    # Rescale boxez from img_size to im0 size
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detecciones por clases
                        s += f"{names[int(c)]}"+" "

                        ##
                        ## escribirReporte(s,str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
                        ##
                        ##
                        # if(prediccion_reciente!=s):
                        #     prediccion_reciente=s
                        #     agregar_reporte("camara_1",
                        #                     str(datetime.now().strftime('%d/%m/%Y %H:%M:%S')),
                        #                     prediccion_reciente)
                        # print(s)
                        
       
                        # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format


                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            annotator.box_label(xyxy, label, color=colors(c, True))


                # Print time (inference-only)
                #LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')
                fecha_hora=str(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
                id_foto=str(datetime.now().strftime('%d%m%Y_%H%M%S'))
                if view_img:
                    im0=cv2.cvtColor(im0,cv2.COLOR_BGR2RGB)
            
                    im0=cv2.putText(im0,estados_conexion["camara_1"]["nombre"], (20,40),cv2.FONT_HERSHEY_TRIPLEX,1,color=(0,0,0),thickness=2)
                    im0=cv2.putText(im0,fecha_hora,(100,40),cv2.FONT_HERSHEY_TRIPLEX,1,color=(0,0,0),thickness=1)
    
                    im=Image.fromarray(im0)
                    img=ImageTk.PhotoImage(image=im)
                    ventana_inicio.camara1.configure(image=img)
                    
                if(prediccion_reciente!=s):
                    prediccion_reciente=s
                    agregar_reporte(camara="camara_1",
                                    ubicacion=estados_conexion["camara_1"]["nombre"],
                                    fecha_hora=fecha_hora,
                                    objetos= prediccion_reciente,
                                    id_imagen=estados_conexion["camara_1"]["nombre"]+"_"+id_foto+".png"
                                    )

                    cv2.imwrite("./registros/imagenes/"+estados_conexion["camara_1"]["nombre"]+"_"+id_foto+".png",im0)
                    print(s)                    
     
        else:
            dataset.cap.release()
            dataset=None
            print("fin de hilo 2")
            break

def cargar_estado_camaras():
    while True:
        time.sleep(1)
        print(ventana_inicio)
        estados_conexion=leer_estado_camaras()
        if (estados_conexion["camara_1"]["estado"]=="conectado"):
            if not(ventana_inicio.inice_antes):
                ventana_inicio.camara1.grid(row=0,column=0)
                ventana_inicio.inice_antes=True
                ##crear el hilo
                hilo2=threading.Thread(name="procesar_imagen",target=procesar_imagen)
                hilo2.start()
        else:
            ventana_inicio.inice_antes=False
        if ventana_inicio.detener_cargar_estado:
            print("fin hilo1")
            break
        print("noo")
        time.sleep(2)


if __name__ == "__main__":
    ventana_inicio=ventana_principal()
    hilo1=threading.Thread(name="ver_datos_camaras",target=cargar_estado_camaras)
    hilo1.start()  
    ventana_inicio.loop()

    

    

    
