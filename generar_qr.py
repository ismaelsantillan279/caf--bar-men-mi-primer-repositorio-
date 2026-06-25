import qrcode
import os
CANT_MESAS = 10
os.makedirs("qr_mesas", exist_ok=True)
for mesa in range(1, CANT_MESAS + 1):
    url = f"https://cafe-bar-menu.onrender.com/?mesa={mesa}"
    qr = qrcode.make(url)
    qr.save(f"qr_mesas/mesa_{mesa}.png")
    print(f"QR mesa {mesa} generado!")

print("¡Todos los QR generados en la carpeta qr_mesas!")