# chatbot/chatbot.py

RESPUESTAS = {

    "saludo":
        "¡Hola! Soy SmartFactoryBot. ¿En qué puedo ayudarte?",

    "soporte_itac":
        (
            "Si tienes problemas con ITAC, valida tu usuario, "
            "contraseña, conexión de red y acceso al servidor. "
            "Si el problema continúa, contacta al equipo Smart Factory."
        ),

    "mes":
        (
            "Verifica que la orden de producción se encuentre activa, "
            "que exista comunicación con MES y que los datos capturados "
            "sean correctos. Si persiste el problema, escala la incidencia."
        ),

    "impresoras":
        (
            "Verifica que la impresora Zebra esté encendida, conectada "
            "a la red, con etiquetas disponibles y sin errores visibles."
        ),

    "scanners":
        (
            "Valida la conexión del scanner, realiza una lectura de prueba "
            "y verifica que el código de barras sea legible."
        ),

    "procedimientos":
        (
            "Consulta la documentación oficial, instructivos y ayudas "
            "visuales disponibles para el proceso solicitado."
        ),

    "escalacion":
        (
            "Si el problema requiere atención inmediata, genera un Andon "
            "o contacta directamente al equipo Smart Factory."
        ),

    "agradecimiento":
        (
            "¡Con gusto! Si necesitas más ayuda, estoy disponible."
        ),

    "despedida":
        (
            "¡Hasta luego! Gracias por utilizar SmartFactoryBot."
        )
}


def responder(intencion):
    """
    Devuelve la respuesta asociada a la intención detectada.
    """

    return RESPUESTAS.get(
        intencion,
        (
            "No encontré información para esta consulta. "
            "Te recomiendo contactar al equipo Smart Factory."
        )
    )


# Prueba local
if __name__ == "__main__":

    print(responder("soporte_itac"))