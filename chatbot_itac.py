import re
import unicodedata
import nltk
from nltk.chat.util import Chat, reflections
import csv
import os
from datetime import datetime

# =========================
# BASE DE CONOCIMIENTO
# =========================

BASE = [

    ('saludo',
     r'^(hola|buenos dias|buenas tardes|buenas noches|hey)\b.*',
     '¡Hola! Soy SmartFactoryBot. ¿En qué puedo ayudarte?'),

    ('soporte_itac',
     r'.*\b(itac|login|acceso|entrar a itac|no puedo ingresar)\b.*',
     'Si no puedes acceder a ITAC, valida usuario, contraseña y conexión de red. Si el problema continúa, contacta a Smart Factory.'),

    ('impresion_etiquetas',
     r'.*\b(etiqueta|etiquetas|impresora|zebra|imprimir)\b.*',
     'Verifica que la impresora esté encendida, conectada y tenga etiquetas disponibles.'),

    ('escaner',
     r'.*\b(escaner|scanner|lector|qr|codigo)\b.*',
     'Revisa la configuración del escáner y valida que el código pueda leerse correctamente.'),

    ('usuarios',
     r'.*\b(usuario|usuarios|acceso|permiso|permisos)\b.*',
     'Para solicitar accesos o permisos, proporciona nombre de usuario y sistema requerido.'),

    ('aplicacion',
     r'.*\b(aplicacion|programa|software|no abre)\b.*',
     'Valida que la aplicación esté instalada correctamente y que tengas acceso a la red.'),

    ('hardware',
     r'.*\b(laptop|computadora|pc|equipo|workstation)\b.*',
     'Las solicitudes de hardware deben realizarse mediante ticket de soporte.'),

    ('trazabilidad',
     r'.*\b(trazabilidad|serial|registro|tracking)\b.*',
     'Verifica que el serial haya sido escaneado correctamente y que la transacción haya sido aceptada por ITAC.'),

    ('numero_parte',
     r'.*\b(numero de parte|part number|material)\b.*',
     'Para agregar un nuevo número de parte se requiere aprobación de Ingeniería de Manufactura.'),

    ('base_datos',
     r'.*\b(base de datos|database|conexion|sql)\b.*',
     'Valida la conectividad al servidor y revisa si existen mantenimientos programados.'),

    ('integracion',
     r'.*\b(integracion|interface|tecnomatix|automatizacion)\b.*',
     'Comparte el mensaje de error y los pasos realizados para revisar la integración.'),

    ('ayuda',
     r'.*\b(ayuda|menu|opciones|que puedes hacer)\b.*',
     'Temas disponibles: ITAC, impresoras, escáneres, trazabilidad, hardware, integraciones y accesos.'),

    ('agradecimiento',
     r'.*\b(gracias|thank you)\b.*',
     '¡De nada! ¿Necesitas ayuda con algo más?'),

    ('despedida',
     r'^(salir|adios|hasta luego)[.!?]*$',
     '¡Hasta luego!'),

    ('vacio',
     r'^$',
     'Por favor escribe una consulta.'),

    ('desconocida',
     r'.*',
     'No identifiqué la consulta. Escribe ayuda para ver las opciones disponibles.')
]

# =========================
# CHATBOT
# =========================

chatbot = Chat(
    [(patron, [respuesta]) for _, patron, respuesta in BASE],
    reflections
)

# =========================
# NORMALIZAR TEXTO
# =========================

def normalizar(texto):

    texto = unicodedata.normalize(
        'NFD',
        texto.lower().strip()
    )

    texto = ''.join(
        c for c in texto
        if unicodedata.category(c) != 'Mn'
    )

    return re.sub(r'\s+', ' ', texto)

# =========================
# RESPONDER
# =========================

def responder(texto):

    limpio = normalizar(texto)

    intencion = next(
        nombre
        for nombre, patron, _ in BASE
        if re.match(
            patron,
            limpio,
            re.IGNORECASE
        )
    )

    return {
        'intencion': intencion,
        'respuesta': chatbot.respond(limpio),
        'texto_normalizado': limpio
    }

# =========================
# GUARDAR EVIDENCIA
# =========================

def guardar_evidencia(
    usuario,
    pregunta,
    resultado
):

    archivo = "evidencias_chatbot.csv"

    existe = os.path.isfile(archivo)

    with open(
        archivo,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as csvfile:

        writer = csv.writer(csvfile)

        if not existe:

            writer.writerow([
                "fecha_hora",
                "usuario",
                "pregunta",
                "texto_normalizado",
                "intencion",
                "respuesta",
                "estado"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            usuario,
            pregunta,
            resultado["texto_normalizado"],
            resultado["intencion"],
            resultado["respuesta"],
            "RESUELTO"
        ])

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    print("=" * 50)
    print(" SMART FACTORY BOT ")
    print("=" * 50)

    print("Versión NLTK:", nltk.__version__)

    usuario = input("\nNombre de usuario: ")

    while True:

        pregunta = input("\nTú: ")

        resultado = responder(pregunta)

        guardar_evidencia(
            usuario,
            pregunta,
            resultado
        )

        print("Intención:", resultado["intencion"])
        print("SmartFactoryBot:", resultado["respuesta"])

        if resultado["intencion"] == "despedida":
            break