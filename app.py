from flask import Flask, render_template

app = Flask(__name__)

class Producto:
    def __init__(self, nombre, precio, categoria):
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
menu = [
    Producto("Café", 3000, "Bebidas Calientes"),
    Producto("Café con leche", 3500, "Bebidas Calientes"),
    Producto("Submarino", 3800, "Bebidas Calientes"),
    Producto("Medialuna", 2000, "Comidas"),
    Producto("Tostado", 4500, "Comidas"),
    Producto("Jugo de naranja", 4000, "Bebidas Frías"),
    Producto("Limonada", 5000, "Bebidas Frías"),
    Producto("Limonada C/frutos rojos", 5300, "Bebidas Frías"),
]

@app.route("/")
def index():
    categorias = {}
    for producto in menu:
        if producto.categoria not in categorias:
            categorias[producto.categoria] = []
        categorias[producto.categoria].append(producto)
    return render_template("index.html", categorias=categorias)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")