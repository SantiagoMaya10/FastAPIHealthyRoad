from fastapi import FastAPI, UploadFile, File, Depends
from PIL import Image
from io import BytesIO
from model.yolov8 import get_external_img_v8
from ultralytics import YOLO
from requestClasses.RequestDepends import DataRoad

# Para obtener swager, se usa localhost:XXXX/docs
app = FastAPI()   

# Cargar el modelo desde el archivo 'best.pt'
modelv8st = YOLO('model/best.pt')

# Start with bash: >>> uvicorn main:app
#                  >>> uvicorn main:app --port $PORT
#                  >>> uvicorn main:app --port $PORT --reload

# Para que se conecten todos los dispositivos que esten en mi red: 
#                   >>> uvicorn main:app --host 0.0.0.0 --port $PORT --reload

# Nombre de la aplicacion
app.title = "Healhty Road API"
app.version = "9.11"


@app.post("/upload", tags=['Load image then classify it and save to database model'])
async def clasify_damage_type_then_save_to_database(file: UploadFile = File(...), 
                  request: DataRoad = Depends()
                  ):
    # Leer el archivo de imagen
    image = Image.open(BytesIO(await file.read()))
    
    # Procesar la imagen usando tu función
    processed_image, L_bboxes, L_danios = get_external_img_v8(modelv8st, image)
    

    # Puedes retornar las cajas delimitadoras y daños, y también guardar la imagen procesada si es necesario
    response = {
        "bboxes": L_bboxes,
        "danios": L_danios
    }
    
    return response