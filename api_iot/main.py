from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_db_connection
from datetime import datetime

# Inicializar la aplicación FastAPI
app = FastAPI(title="API IoT - Sensores", version="1.0.0")

# Modelo de datos que esperamos recibir del ESP32 (Formato JSON)
class LecturaIoT(BaseModel):
    temperatura: float
    humedad: float
    lluvia: float

@app.get("/")
def read_root():
    return {"message": "La API está funcionando correctamente. Ve a /docs para ver la interfaz."}

@app.post("/api/v1/readings/", status_code=201)
def create_reading(lectura: LecturaIoT):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Error de conexión a la BD")
    
    cursor = conn.cursor()
    try:
        tiempo_actual = datetime.now()
        
        # En nuestra base de datos, asociaremos:
        # sensor_id 1 = Temperatura
        # sensor_id 2 = Humedad
        # sensor_id 3 = Lluvia
        
        query = """
        INSERT INTO lecturas (tiempo, sensor_id, valor) VALUES 
        (%s, 1, %s),
        (%s, 2, %s),
        (%s, 3, %s)
        """
        cursor.execute(query, (
            tiempo_actual, lectura.temperatura,
            tiempo_actual, lectura.humedad,
            tiempo_actual, lectura.lluvia
        ))
        
        conn.commit()
        return {"status": "success", "message": "Lecturas registradas con éxito"}
        
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
