import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def get_db_connection():
    try:
        # Nos conectamos usando la variable DATABASE_URL
        conn = psycopg2.connect(
            os.environ.get("DATABASE_URL"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        return None
