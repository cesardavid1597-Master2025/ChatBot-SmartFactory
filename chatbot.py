import re
import unicodedata
import nltk
from nltk.chat.util import Chat, reflections

BASE = [
    ('saludo', r'^(hola|buenos dias|buenas tardes|buenas noches|hey)\b.*',
     '¡Hola! Soy OrientaBot. Consulta sobre inscripciones, horarios, becas o constancias.'),

    ('inscripcion', r'.*\b(inscripcion|inscripciones|inscribirme|reinscripcion)\b.*',
     'Consulta la convocatoria vigente y contacta a Control Escolar para conocer el proceso de inscripción o reinscripción. Verifica allí fechas y requisitos oficiales.'),

    ('horarios', r'.*\b(horario|horarios|clases)\b.*',
     'Consulta tu horario en el sistema escolar institucional. Si existe algún problema con tu grupo o materia, contacta a Control Escolar.'),

    ('becas', r'.*\b(beca|becas|apoyo economico)\b.*',
     'Consulta las convocatorias institucionales vigentes. El área de Becas puede orientarte sobre requisitos, documentos y fechas.'),

    ('constancias', r'.*\b(constancia|constancias|comprobante de estudios)\b.*',
     'Solicita información a Control Escolar sobre el procedimiento, documentos necesarios y tiempo de entrega de constancias.'),

    ('control_escolar', r'.*\b(control escolar|servicios escolares)\b.*',
     'Control Escolar orienta sobre trámites académicos. Consulta sus medios de contacto en el sitio oficial de tu institución.'),

    ('ayuda', r'.*\b(ayuda|menu|opciones|que puedes hacer)\b.*',
     'Temas disponibles: inscripciones, horarios, becas, constancias y Control Escolar. Escribe salir para terminar.'),

    ('agradecimiento', r'.*\bgracias\b.*',
     '¡De nada! ¿Necesitas orientación sobre otro tema?'),

    ('despedida', r'^(salir|adios|hasta luego)[.!?]*$',
     '¡Hasta luego! Gracias por consultar OrientaBot.'),

    ('vacio', r'^$',
     'Escribe una consulta para poder orientarte.'),

    ('desconocida', r'.*',
     'No identifiqué tu consulta. Intenta mencionar inscripciones, horarios, becas, constancias o Control Escolar.')
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