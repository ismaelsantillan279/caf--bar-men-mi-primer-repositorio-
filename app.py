from flask import Flask, render_template, request, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = "cafebar2024"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Contraseña incorrecta")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    productos_db = database.obtener_productos()
    categorias = {}
    for nombre, precio, categoria in productos_db:
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append({"nombre": nombre, "precio": precio})
    return render_template("index.html", categorias=categorias)

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("login"))
    con = database.conectar()
    cursor = con.cursor()
    cursor.execute("SELECT id, nombre, precio, categoria FROM productos ORDER BY categoria")
    productos = cursor.fetchall()
    con.close()
    return render_template("admin.html", productos=productos)

@app.route("/admin/agregar", methods=["POST"])
def agregar():
    if not session.get("admin"):
        return redirect(url_for("login"))
    nombre = request.form["nombre"]
    precio = int(request.form["precio"])
    categoria = request.form["categoria"]
    database.agregar_producto(nombre, precio, categoria)
    return redirect(url_for("admin"))

@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = int(request.form["precio"])
        categoria = request.form["categoria"]
        database.editar_producto(id, nombre, precio, categoria)
        return redirect(url_for("admin"))
    producto = database.obtener_producto_por_id(id)
    return render_template("editar.html", producto=producto)

@app.route("/admin/borrar/<int:id>")
def borrar(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    database.borrar_producto(id)
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")