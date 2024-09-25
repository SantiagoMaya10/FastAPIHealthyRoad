from fastapi import FastAPI, UploadFile, File, Depends
from PIL import Image
from io import BytesIO
from model.yolov8 import get_external_img_v8, get_name_file, get_tramo_ini_fin
from ultralytics import YOLO
from requestClasses.RequestDepends import DataRoad
from datetime import datetime

# Para obtener swager, se usa localhost:XXXX/docs
# Para obtener otro tipo de documentacion: localhost:XXXX/redoc
app = FastAPI()   

# Cargar el modelo desde el archivo 'best.pt'
modelv8st = YOLO('model/best.pt')

# Start with bash: >>> uvicorn main:app
#                  >>> uvicorn main:app --port 1802
#                  >>> uvicorn main:app --port 1802 --reload

# Para que se conecten todos los dispositivos que esten en mi red: 
#                   >>> uvicorn main:app --host 0.0.0.0 --port 1802 --reload

# Nombre de la aplicacion
app.title = "Healhty Road API"
app.version = "9.11"


@app.post("/upload", tags=['Load image and return model prediction'])
async def predict_damage_type(file: UploadFile = File(...), 
                  request: DataRoad = Depends()
                  ):
    # Leer el archivo de imagen
    image = Image.open(BytesIO(await file.read()))
    
    # Procesar la imagen usando tu función
    processed_image, L_bboxes, L_danios = get_external_img_v8(modelv8st, image)
    
    # PARA EL NOMBRE DEL ARCHIVO

    # Acceder a los parámetros adicionales
    tramo_ini,tramo_final=get_tramo_ini_fin(request.latitud, request.longitud)

    # Obtener la fecha y hora actual
    fecha_actual = datetime.now()

    # Formatear la fecha en el formato deseado con milisegundos, el procesamiento es rápido, por
    # lo que puede haber concurrencia de imagenes sino se anaden los milisegundos
    fecha_formateada = fecha_actual.strftime("%Y%m%d_%H%M%S") + f"_{fecha_actual.microsecond // 1000:03d}"

    # Guardar imagen en la raiz de donde fue pedido.
    file_name=get_name_file(file.filename)

    ## Commented line because if image is saved the cloud service runs put of memory                    
    ## processed_image.save(f"saveImgPredict/{file_name}_{tramo_ini+tramo_final}_{fecha_formateada}.jpg")

    # Puedes retornar las cajas delimitadoras y daños, y también guardar la imagen procesada si es necesario
    response = {
        "bboxes": L_bboxes,
        "danios": L_danios
    }
    
    return response