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

def agregar_producto(nombre, precio, categoria):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO productos (nombre, precio, categoria) VALUES  (%s, %s, %s)", (nombre, precio, categoria)
    )
    con.commit()
    con.close()

def editar_producto(id, nombre, precio, categoria):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "UPDATE productos SET nombre=%s, precio=%s, categoria=%s  WHERE id=%s", (nombre, precio, categoria, id)
    )
    con.commit()
    con.close()

def borrar_producto(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    con.commit()
    con.close()

def obtener_producto_por_id(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre, precio, categoria FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    con.close()
    return producto

def crear_tabla_pedidos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS pedidos (
                   id SERIAL PRIMARY KEY,
                   mesa INTEGER NOT NULL,
                   productos TEXT NOT NULL,
                   total INTEGER NOT NULL,
                   estado TEXT DEFAULT 'pendiente',
                   fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )""")
    con.commit()
    con.close()

def guardar_pedido(mesa, productos, total):
    con = conectar()
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO pedidos (mesa, productos, total) VALUES (%s, %s, %s)", (mesa, productos, total)
    )
    con.commit()
    con.close()

def obtener_pedidos():
    con = conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, mesa, productos, total, estado, fecha FROM pedidos WHERE estado='pendiente' ORDER BY fecha")
    pedidos = cursor.fetchall()
    con.close()
    return pedidos

def marcar_entregado(id):
    con = conectar()
    cursor = con.cursor()
    cursor.execute("UPDATE pedidos SET estado='entregado' WHERE id=%s", (id,))
    con.commit()
    con.close()
    
crear_tabla()
insertar_productos_iniciales()
crear_tabla_pedidos()