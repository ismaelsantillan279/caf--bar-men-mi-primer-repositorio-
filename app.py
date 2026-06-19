from flask import Flask, render_template
import database
app = Flask(__name__)

@app.route("/")
def index():
    productos_db = database.obtener_productos()
    categorias = {}
    for nombre, precio, categoria in productos_db:
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append({"nombre": nombre, "precio": precio})
    return render_template("index.html", categorias=categorias)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")