from flask import Flask, render_template, request, redirect, url_for, session
import os
import database

app = Flask(__name__)
app.secret_key = "cafebar2024"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
            password_actual = database.obtener_password()
            if request.form["password"] == password_actual:
                session["admin"] = True
                return redirect(url_for("admin"))
            else:
                return render_template("login.html", error="Contraseña incorrecta")
    return render_template("login.html", error=None)

@app.route("/admin/cambiar-password", methods=["GET", "POST"])
def cambiar_password():
    if not session.get("admin"):
        return redirect(url_for("login"))
    if request.method == "POST":
        password_actual = database.obtener_password()
        actual = request.form["actual"]
        nueva = request.form["nueva"]
        repetir = request.form["repetir"]

        if actual != password_actual:
            return render_template("cambiar_password.html", error="La contraseña actual es incorrecta")
        if nueva != repetir:
            return render_template("cambiar_password.html", error="Las contraseñas nuevas no coinciden")
        if len(nueva) < 6:
            return render_template("cambiar_password.html", error="La contraseña debe tener al menos 6 caracteres")
        
        database.cambiar_password(nueva)
        return render_template("cambiar_password.html", exito="¡Contraseña cambiada correctamente!")
    
    return render_template("cambiar_password.html", error=None)
 
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))

@app.route("/")
def index():
    productos_db = database.obtener_productos()
    categorias = {}
    for nombre, precio, categoria, imagen in productos_db:
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append({"nombre": nombre, "precio": precio, "imagen": imagen})
    return render_template("index.html", categorias=categorias)

@app.route("/confirmar", methods=["POST"])
def confirmar():
    print("LLEGÓ A CONFIRMAR")
    mesa = request.form.get("mesa", "0")
    productos = request.form.get("productos")
    total = int(request.form.get("total"))
    database.guardar_pedido(mesa, productos, total)
    return render_template("factura.html", mesa=mesa, productos=productos, total=total)

@app.route("/admin/pedidos")
def pedidos():
    if not session.get("admin"):
        return redirect(url_for("login"))
    pedidos = database.obtener_pedidos()
    return render_template("pedidos.html", pedidos=pedidos)

@app.route("/admin/pedidos/entregar/<int:id>")
def entregar(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    database.marcar_entregado(id)
    return redirect(url_for("pedidos"))

@app.route("/admin/historial")
def historial():
    if not session.get("admin"):
        return redirect(url_for("login"))
    pedidos = database.obtener_historial()
    return render_template("historial.html", pedidos=pedidos)

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

    imagen_archivo = request.files.get("imagen")
    nombre_imagen = None

    if imagen_archivo and imagen_archivo.filename != "":
        nombre_imagen = imagen_archivo.filename
        ruta = os.path.join("static", "imagenes", nombre_imagen)
        imagen_archivo.save(ruta)

    database.agregar_producto(nombre, precio, categoria, nombre_imagen)
    return redirect(url_for("admin"))

@app.route("/admin/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = int(request.form["precio"].replace(".", ""))
        categoria = request.form["categoria"]
        
        imagen_archivo = request.files.get("imagen")
        nombre_imagen = None
        
        if imagen_archivo and imagen_archivo.filename != "":
            nombre_imagen = imagen_archivo.filename
            ruta = os.path.join("static", "imagenes", nombre_imagen)
            imagen_archivo.save(ruta)
        
        database.editar_producto(id, nombre, precio, categoria, nombre_imagen)
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