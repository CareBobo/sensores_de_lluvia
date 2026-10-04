import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    cursor = conn.cursor()
    
    # 1. Insertar ubicación
    cursor.execute("INSERT INTO ubicaciones (id, nombre) VALUES (1, 'Laboratorio') ON CONFLICT (id) DO NOTHING;")
    
    # 2. Insertar dispositivo
    cursor.execute("INSERT INTO dispositivos (id, mac_address, nombre, ubicacion_id) VALUES (1, '00:11:22:33:44:55', 'ESP32 Principal', 1) ON CONFLICT (id) DO NOTHING;")
    
    # 3. Insertar tipos de sensores
    cursor.execute("INSERT INTO tipos_sensores (id, nombre) VALUES (1, 'DHT22 Temp'), (2, 'DHT22 Hum'), (3, 'Sensor Lluvia') ON CONFLICT (id) DO NOTHING;")
    
    # 4. Insertar unidades de medida
    cursor.execute("INSERT INTO unidades_medida (id, simbolo, nombre) VALUES (1, 'C', 'Celsius'), (2, '%', 'Porcentaje'), (3, 'Analog', 'Analógico') ON CONFLICT (id) DO NOTHING;")
    
    # 5. Insertar sensores
    cursor.execute("""
        INSERT INTO sensores (id, dispositivo_id, tipo_sensor_id, unidad_medida_id, pin_conexion) 
        VALUES 
        (1, 1, 1, 1, 'GPIO 4'), 
        (2, 1, 2, 2, 'GPIO 4'), 
        (3, 1, 3, 3, 'GPIO 34') 
        ON CONFLICT (id) DO NOTHING;
    """)
    
    conn.commit()
    print("Datos iniciales insertados correctamente.")
except Exception as e:
    if 'conn' in locals() and conn:
        conn.rollback()
    print("Error:", e)
finally:
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
