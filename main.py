from chatbot_itac  import responder

print("=================================")
print("      Bienvenido a OrientaBot")
print("=================================")
print("Escribe 'salir' para terminar.\n")

while True:
    mensaje = input("Tú: ")

    if mensaje.lower() == "salir":
        print("OrientaBot: ¡Hasta luego!")
        break

    respuesta = responder(mensaje)

    print("OrientaBot:", respuesta["respuesta"])
