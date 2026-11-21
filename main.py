# main.py

import csv
from datetime import datetime
from pathlib import Path

from chatbot.prediccion import predecir_intencion
from chatbot.chatbot import responder

# ==========================================
# ARCHIVO DE LOG
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

ARCHIVO_LOG = (
    BASE_DIR /
    "data" /
    "conversaciones.csv"
)

# Crear archivo si no existe
if not ARCHIVO_LOG.exists():

    with open(
        ARCHIVO_LOG,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as archivo:

        writer = csv.writer(archivo)

        writer.writerow(
            [
                "fecha_hora",
                "pregunta",
                "intencion",
                "respuesta"
            ]
        )

# ==========================================
# CHATBOT
# ==========================================

print("=" * 60)
print("SMARTFACTORYBOT")
print("=" * 60)

print("\nEscribe tu consulta.")
print("Escribe 'salir' para finalizar.\n")

while True:

    pregunta = input("Tú: ").strip()

    if pregunta.lower() in [
        "salir",
        "adios",
        "exit"
    ]:

        print(
            "\nSmartFactoryBot:"
            " ¡Hasta luego!"
        )

        break

    try:

        intencion = predecir_intencion(
            pregunta
        )

        respuesta = responder(
            intencion
        )

        print(
            f"\nIntención detectada: "
            f"{intencion}"
        )

        print(
            f"SmartFactoryBot: "
            f"{respuesta}\n"
        )

        # ==========================
        # GUARDAR HISTORIAL
        # ==========================

        with open(
            ARCHIVO_LOG,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as archivo:

            writer = csv.writer(archivo)

            writer.writerow(
                [
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    pregunta,
                    intencion,
                    respuesta
                ]
            )

    except Exception as e:

        print(
            "\nSmartFactoryBot:"
            " Error procesando consulta."
        )

        print(f"\nDetalle: {e}")