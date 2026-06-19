import database

productos = database.obtener_productos()
for p in productos:
    print(p)