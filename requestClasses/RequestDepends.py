from pydantic import BaseModel

# Definir el modelo de 'location'
class DataRoad(BaseModel):
    latitud: str
    longitud: str
    road_id: int