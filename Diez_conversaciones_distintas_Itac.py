from chatbot_itac import responder

CONVERSACIONES = [
    [
        ('¿Por qué no imprime la etiquetadora?', 'impresion_etiquetas')
    ],
    [
        ('No puedo ingresar a ITAC', 'soporte_itac')
    ],
    [
        ('Mi escáner Zebra no lee códigos QR', 'escaner')
    ],
    [
        ('Necesito crear un nuevo usuario en el sistema', 'usuarios')
    ],
    [
        ('La aplicación de producción no abre', 'aplicacion')
    ],
    [
        ('¿Cómo solicito una nueva estación de trabajo?', 'hardware')
    ],
    [
        ('No se están registrando las trazabilidades', 'trazabilidad')
    ],
    [
        ('¿Cómo agrego un nuevo número de parte en ITAC?', 'numero_parte')
    ],
    [
        ('El sistema muestra error de conexión con la base de datos', 'base_datos')
    ],
    [
        ('Necesito ayuda con una integración de producción', 'integracion')
    ]
]

registros = []

for numero, conversacion in enumerate(CONVERSACIONES, 1):
    print(f'\n=== Conversación {numero:02d} ===')

    for entrada, esperada in conversacion:
        salida = responder(entrada)
        correcto = salida['intencion'] == esperada

        registros.append({
            'conversacion': numero,
            'entrada': entrada,
            'esperada': esperada,
            **salida,
            'correcto': correcto
        })

        print('Usuario:', repr(entrada))
        print('SmartFactoryBot:', salida['respuesta'])
        print(
            'Intención:', salida['intencion'],
            '| Resultado:', 'OK' if correcto else 'REVISAR'
        )

aciertos = sum(r['correcto'] for r in registros)

print(f'\nResultado: {aciertos}/{len(registros)} turnos coinciden con lo esperado.')

assert aciertos == len(registros), 'Hay casos que requieren revisión.'
