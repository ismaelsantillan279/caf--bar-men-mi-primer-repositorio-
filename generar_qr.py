import qrcode

# generamos el QR con la URL de tu página
qr = qrcode.make("https://cafe-bar-menu.onrender.com")

# lo guardamos como imagen
qr.save("menu_qr.png")
print("QR generado!")