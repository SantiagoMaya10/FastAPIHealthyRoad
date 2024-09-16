from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd
from model.constants import id2Labelv8s, COLORS_V8S


# Funcion para determinar si es un numero o no
def isInteger(str):
    try:
        int(str)
        return True
    except:
        return False

# Funcion para obtener tramo inicial y final
def get_tramo_ini_fin(lat, lon):
    # Realizar un split por espacios en blanco a la cadena
    split_lat = lat.split(" ")
    split_lon = lon.split(" ")

    # Obtener los numeros, se obtendra la coordenada como el primer elemento
    list_lat_number = list(filter(
        lambda x: isInteger(x), split_lat
    ))
    list_lon_number = list(filter(
        lambda x: isInteger(x), split_lon
    ))

    # Si alguna lista esta vacia
    if(len(list_lat_number)==0 or len(list_lon_number)==0):
        return ("0","0")
    else:   
        # Obtener el primer elemento de cada lista
        f_lat=list_lat_number[0]
        f_lon=list_lon_number[0]

        # Regresarlos como una tupla de strings
        return (str(f_lat),str(f_lon))

# Funcion para obtener nombre del archivo dado un path
def get_name_file(path):
    l=path.split("/")
    return l[len(l)-1].split(".")[0]

def get_pred_with_output_v8(model, dataset, index, use_dataset=True, L=[]):
    # Cargar la imagen

    if use_dataset:
        # Si usa un dataset cargado por DataLoader
        image_ids = dataset.coco.getImgIds()
        image_id = image_ids[index]
        image_info = dataset.coco.loadImgs(image_id)[0]
        print(image_info['file_name'])

        image = Image.open(os.path.join("RDDD2022/Img/", image_info['file_name']))
    else:
        # Si usa una imagen de forma externa
        image = L[0]

    # Crear dataframe auxiliar para guardar los valores de las predicciones
    best_bboxes = pd.DataFrame(columns=['xmin', 'ymin', 'xmax', 'ymax','confidence','name'])

    # Realizar predicción utilizando el modelo YOLOv8
    results = model(image)
    for result in results:
        # Por cada resultado del conjunto de resultados

        # Obtener todos los bounding boxes
        boxes = result.boxes
        for box in boxes:
            # Por cada bounding box

            # Obtener coordenadas y la clase, moviéndolas a la CPU y convirtiéndolas a numpy
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # Coordenadas del bounding box
            class_id = int(box.cls[0].cpu().numpy())  # ID de la clase predicha
            score = float(box.conf[0].cpu().numpy())  # Confianza de la predicción

            # Guardar en el dataframe
            best_bboxes.loc[len(best_bboxes)]=(x1,y1,x2,y2,score,id2Labelv8s[class_id])
            #print(box.conf)
   
    # Definir el tamaño del texto
    font_size = 18
    
    try:
        # Cargar una fuente TrueType del sistema con el tamaño deseado
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Si no se encuentra la fuente TrueType, usar la fuente por defecto
        font = ImageFont.load_default()
        
    # Convertir resultados a listas de coordenadas y etiquetas
    L_bboxes = best_bboxes[['xmin', 'ymin', 'xmax', 'ymax']].values.tolist()
    L_danios = [
        f"{row['name']}"
        #: {row['confidence']:.2f}" 
        for _, row in best_bboxes.iterrows()
    ]

    # Mov Y
    movy=20
    
    # Dibujar los resultados sobre la imagen
    draw = ImageDraw.Draw(image)
    for bbox, label in zip(L_bboxes, L_danios):
        xmin, ymin, xmax, ymax = bbox

        # Dibujar rectángulo
        draw.rectangle([(xmin, ymin), (xmax, ymax)], outline=COLORS_V8S[label.split(": ")[0]], width=4)

        # Calcular el tamaño del fondo del texto
        text_bbox = draw.textbbox((xmin, ymin-movy), label, font=font)
        # Dibujar el fondo blanco del texto
        draw.rectangle(text_bbox, fill="white")

        draw.text((xmin, ymin-movy), label, fill=COLORS_V8S[label.split(": ")[0]], font=font)
        #draw.text((xmin, ymin), label, fill="black", textsize=50)

    return image, L_bboxes, L_danios


def get_external_img_v8(model, image):
    
    # Cargar la imagen
    # image = Image.open(image_path)

    # Realizar predicción utilizando el modelo YOLOv8
    image, L_bboxes, L_danios = get_pred_with_output_v8(model,
                                                        dataset=None,
                                                        index=None,
                                                        use_dataset=False,
                                                        L=[image])

    return image, L_bboxes, L_danios