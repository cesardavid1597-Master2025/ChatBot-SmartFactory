import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from chatbot.preprocesamiento import preprocesar

from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================
# RUTAS DEL PROYECTO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = BASE_DIR / "data" / "dataset.csv"

MODELO = BASE_DIR / "modelos" / "modelo_nb.pkl"

VECTORIZADOR = BASE_DIR / "modelos" / "vectorizador_tfidf.pkl"


# ==========================================
# CARGA DE DATOS
# ==========================================

print("\n==============================")
print("Cargando dataset...")
print("==============================")

df = pd.read_csv(DATASET)

print(f"\nCantidad de registros: {len(df)}")

print("\nDistribución de intenciones:")
print(df["intencion"].value_counts())

# ==========================================
# PREPROCESAMIENTO
# ==========================================

print("\n==============================")
print("Preprocesando texto...")
print("==============================")

df["texto_procesado"] = df["texto"].apply(preprocesar)

print("\nEjemplos procesados:")

for i in range(min(5, len(df))):
    print(f"\nOriginal:   {df.iloc[i]['texto']}")
    print(f"Procesado: {df.iloc[i]['texto_procesado']}")

# ==========================================
# VARIABLES DE ENTRENAMIENTO
# ==========================================

X = df["texto_procesado"]
y = df["intencion"]

# ==========================================
# TF-IDF
# ==========================================

print("\n==============================")
print("Aplicando TF-IDF...")
print("==============================")

vectorizador = TfidfVectorizer(
    ngram_range=(1,2),
    min_df=2
)

X_tfidf = vectorizador.fit_transform(X)

print(f"\nCantidad de términos únicos: {len(vectorizador.get_feature_names_out())}")

# ==========================================
# DIVISIÓN DE DATOS
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nRegistros entrenamiento: {X_train.shape[0]}")
print(f"Registros prueba: {X_test.shape[0]}")

# ==========================================
# ENTRENAMIENTO
# ==========================================

print("\n==============================")
print("Entrenando Naive Bayes...")
print("==============================")

modelo = LinearSVC()

modelo.fit(X_train, y_train)

# ==========================================
# PREDICCIONES
# ==========================================

predicciones = modelo.predict(X_test)

# ==========================================
# MÉTRICAS
# ==========================================

accuracy = accuracy_score(y_test, predicciones)

print("\n==============================")
print("RESULTADOS")
print("==============================")

print(f"\nAccuracy: {accuracy:.2%}")

print("\nReporte de clasificación:")
print(
    classification_report(
        y_test,
        predicciones,
        zero_division=0
    )
)

print("\nMatriz de confusión:")

etiquetas = sorted(y.unique())

matriz = confusion_matrix(
    y_test,
    predicciones,
    labels=etiquetas
)

matriz_df = pd.DataFrame(
    matriz,
    index=etiquetas,
    columns=etiquetas
)

print(matriz_df)


# ==========================================
# TIMESTAMP
# ==========================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ==========================================
# RUTAS EVIDENCIAS
# ==========================================

EVIDENCIAS = BASE_DIR / "evidencias"
EVIDENCIAS.mkdir(exist_ok=True)

REPORTE_TXT = EVIDENCIAS / f"reporte_modelo_{timestamp}.txt"
REPORTE_EXCEL = EVIDENCIAS / f"metricas_modelo_{timestamp}.xlsx"
GRAFICA_PNG = EVIDENCIAS / f"matriz_confusion_{timestamp}.png"

# ==========================================
# REPORTE TXT
# ==========================================

with open(REPORTE_TXT, "w", encoding="utf-8") as archivo:

    archivo.write("REPORTE DE ENTRENAMIENTO\n")
    archivo.write("=" * 60 + "\n\n")

    archivo.write(f"Fecha: {datetime.now()}\n\n")

    archivo.write(f"Cantidad de registros: {len(df)}\n\n")

    archivo.write("Distribución de intenciones:\n")
    archivo.write(str(df["intencion"].value_counts()))
    archivo.write("\n\n")

    archivo.write(f"Accuracy: {accuracy:.2%}\n\n")

    archivo.write("REPORTE DE CLASIFICACION\n")
    archivo.write(
        classification_report(
            y_test,
            predicciones,
            zero_division=0
        )
    )

    archivo.write("\n\nMATRIZ DE CONFUSION\n")
    archivo.write(str(matriz_df))

# ==========================================
# EXCEL
# ==========================================

reporte_dict = classification_report(
    y_test,
    predicciones,
    output_dict=True
)

metricas_df = pd.DataFrame(reporte_dict).transpose()

with pd.ExcelWriter(REPORTE_EXCEL) as writer:

    metricas_df.to_excel(
        writer,
        sheet_name="Metricas"
    )

    matriz_df.to_excel(
        writer,
        sheet_name="Matriz_Confusion"
    )
    resumen_df = pd.DataFrame([
        {
            "Fecha": datetime.now(),
            "Accuracy": accuracy,
            "Registros": len(df),
            "Terminos_TFIDF": len(
                vectorizador.get_feature_names_out()
            )
        }
    ])

    resumen_df.to_excel(
        writer,
        sheet_name="Resumen",
        index=False
    )

    

# ==========================================
# GRAFICA PNG
# ==========================================

plt.figure(figsize=(10, 8))

sns.heatmap(
    matriz_df,
    annot=True,
    fmt="d",
    cmap="Blues"
)

plt.title(
    f"Matriz de Confusión\nAccuracy = {accuracy:.2%}"
)

plt.xlabel("Predicción")
plt.ylabel("Valor Real")

plt.tight_layout()

plt.savefig(
    GRAFICA_PNG,
    dpi=300
)

plt.close()

# ==========================================
# GUARDAR MODELO
# ==========================================

joblib.dump(modelo, MODELO)

joblib.dump(vectorizador, VECTORIZADOR)

print("\n==============================")
print("ARCHIVOS GENERADOS")
print("==============================")

print(f"\nReporte TXT:")
print(REPORTE_TXT)

print(f"\nExcel:")
print(REPORTE_EXCEL)

print(f"\nGráfica:")
print(GRAFICA_PNG)

print(f"\nAccuracy: {accuracy:.2%}")

print("\n✅ Modelo entrenado correctamente.")