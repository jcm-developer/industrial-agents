import sqlite3
import pandas as pd

DB_NAME = 'industrial_predictions.db'

def init_db():
    """
    Inicializa la base de datos y crea la tabla si no existe.
    """    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS industrial_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            client_req TEXT,
            first_review TEXT,
            second_review TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_prediction(client_req, first_review, second_review):
    """
    Guarda una nueva predicción en la base de datos.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO industrial_predictions (client_req, first_review, second_review) 
        VALUES (?, ?, ?)
    ''', (client_req, first_review, second_review))
    conn.commit()
    conn.close()

def get_history():
    """
    Devuelve todas las predicciones como un DataFrame de Pandas.
    """
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT date, client_req, first_review, second_review FROM industrial_predictions ORDER BY id DESC", conn)
        return df
    except:
        return pd.DataFrame()
    finally:
        conn.close()