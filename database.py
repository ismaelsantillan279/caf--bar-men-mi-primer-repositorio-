import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def conectar():
    return psycopg2.connect(os.getenv("DATABASE_URL"))
def crear_tabla():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS productos(
                   id SERIAL PRIMARY KEY,
                   nombre TEXT NOT NULL,
                   precio INTEGER NOT NULL,
                   categoria TEXT NOT NULL
                   )
  """)
    con.commit()
    con.close()

def insertar_productos_iniciales():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos = [
            ("Café", 3000, "Bebidas Calientes"),
            ("Café con leche", 3500, "Bebidas Calientes"),
            ("Submarino", 3800, "Bebidas Calientes"),
            ("Medialuna", 2000, "Comidas"),
            ("Tostado", 4500, "Comidas"),
            ("Jugo de naranja", 4000, "Bebidas Frías"),
            ("Limonada", 5000, "Bebidas Frías"),
            ("Limonada C/frutos rojos", 5300, "Bebidas Frías"),
        ]
        cursor.executemany(
            "INSERT INTO productos (nombre, precio, categoria) VALUES (%s, %s, %s)", productos
        )
        con.commit()
    con.close()

def obtener_productos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT nombre, precio, categoria FROM productos ORDER BY categoria")
    productos = cursor.fetchall()
    con.close()
    return productos
crear_tabla()
insertar_productos_iniciales()