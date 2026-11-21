from pathlib import Path

# Ruta raíz del proyecto
BASE_DIR = Path(
    r"C:\Users\sesa724651\OneDrive - Schneider Electric\Personal Cesar Diaz\Documentos TEC Milenio\Bimestre 2\ChatBotSmartFactory"
)

# Carpetas
carpetas = [
    "chatbot",
    "data",
    "modelos",
    "evidencias"
]

# Archivos
archivos = [
    "main.py",
    "requirements.txt",

    "chatbot/__init__.py",
    "chatbot/chatbot.py",
    "chatbot/preprocesamiento.py",
    "chatbot/entrenamiento.py",
    "chatbot/prediccion.py",

    "data/dataset.csv",
    "data/conversaciones.csv"
]

print(f"\nCreando estructura en:\n{BASE_DIR}\n")

# Crear carpetas
for carpeta in carpetas:
    ruta = BASE_DIR / carpeta
    ruta.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Carpeta: {ruta}")

# Crear archivos
for archivo in archivos:
    ruta = BASE_DIR / archivo

    if not ruta.exists():
        ruta.touch()
        print(f"[OK] Archivo: {ruta}")
    else:
        print(f"[EXISTE] Archivo: {ruta}")

print("\n✅ Estructura creada correctamente.")