# chatbot/prediccion.py

import joblib
from pathlib import Path

from chatbot.preprocesamiento import preprocesar


# ==========================================
# RUTAS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELO_PATH = BASE_DIR / "modelos" / "modelo_nb.pkl"

VECTORIZADOR_PATH = (
    BASE_DIR / "modelos" / "vectorizador_tfidf.pkl"
)

# ==========================================
# CARGA DE MODELO Y VECTORIZADOR
# ==========================================

modelo = joblib.load(MODELO_PATH)

vectorizador = joblib.load(VECTORIZADOR_PATH)


# ==========================================
# PREDICCIÓN
# ==========================================

def predecir_intencion(texto):

    texto_procesado = preprocesar(texto)

    vector = vectorizador.transform(
        [texto_procesado]
    )

    intencion = modelo.predict(vector)[0]

    return intencion


# ==========================================
# PRUEBAS
# ==========================================

if __name__ == "__main__":

    pruebas = [
        "no puedo entrar a itac",
        "la zebra no imprime etiquetas",
        "error en mes",
        "scanner no funciona",
        "como levantar un andon",
        "gracias por tu ayuda",
        "hasta luego"
    ]

    print("\nPRUEBAS DEL MODELO\n")

    for texto in pruebas:

        prediccion = predecir_intencion(texto)

        print(
            f"Texto: {texto}\n"
            f"Intención: {prediccion}\n"
        )