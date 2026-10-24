import re
import unicodedata
import nltk
from nltk.chat.util import Chat, reflections
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
chatbot = Chat(
    [(patron, [respuesta]) for _, patron, respuesta in BASE],
    reflections
)

def normalizar(texto):
    texto = unicodedata.normalize('NFD', texto.lower().strip())
    texto = ''.join(
        c for c in texto
        if unicodedata.category(c) != 'Mn'
    )
    return re.sub(r'\s+', ' ', texto)

def responder(texto):
    limpio = normalizar(texto)

    intencion = next(
        nombre
        for nombre, patron, _ in BASE
        if re.match(patron, limpio, re.IGNORECASE)
    )

    return {
        'intencion': intencion,
        'respuesta': chatbot.respond(limpio)
    }

for nombre, patron, respuesta in BASE:
    print(f'{nombre}: {respuesta}')

print('Versión NLTK:', nltk.__version__)

while True:
    pregunta = input("\nTú: ")

    if pregunta.lower() == "salir":
        print("OrientaBot: ¡Hasta luego!")
        break

    resultado = responder(pregunta)

    print("Intención:", resultado["intencion"])
    print("OrientaBot:", resultado["respuesta"])

if __name__ == "__main__":
    print('Versión NLTK:', nltk.__version__)

    while True:
        pregunta = input("\nTú: ")

        if pregunta.lower() == "salir":
            print("OrientaBot: ¡Hasta luego!")
            break

        resultado = responder(pregunta)

        print("Intención:", resultado["intencion"])
        print("OrientaBot:", resultado["respuesta"])