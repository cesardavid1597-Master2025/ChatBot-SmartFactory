import re
import unicodedata
import nltk

# Ruta local donde colocaste los recursos NLTK
nltk.data.path.append(
    r"C:\Users\sesa724651\nltk_data"
)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SpanishStemmer

# Recursos
stop_words = set(stopwords.words("spanish"))
stemmer = SpanishStemmer()


def normalizar(texto):
    """
    Convierte a minúsculas, elimina acentos y caracteres especiales.
    """

    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    texto = re.sub(r"[^a-zA-Zñ\s]", " ", texto)

    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def tokenizar(texto):
    """
    Divide el texto en palabras.
    """

    return word_tokenize(texto, language="spanish")


def eliminar_stopwords(tokens):
    """
    Elimina palabras vacías.
    """

    return [
        token
        for token in tokens
        if token not in stop_words
    ]


def aplicar_stemming(tokens):
    """
    Aplica stemming usando Snowball para español.
    """

    return [
        stemmer.stem(token)
        for token in tokens
    ]


def preprocesar(texto):
    """
    Pipeline completo:
    1. Normalización
    2. Tokenización
    3. Stopwords
    4. Stemming
    """

    texto = normalizar(texto)

    tokens = tokenizar(texto)

    tokens = eliminar_stopwords(tokens)

    tokens = aplicar_stemming(tokens)

    return " ".join(tokens)


if __name__ == "__main__":

    ejemplo = "¡No puedo entrar a ITAC porque me marca error de usuario!"

    print("Texto original:")
    print(ejemplo)

    print("\nNormalizado:")
    print(normalizar(ejemplo))

    tokens = tokenizar(normalizar(ejemplo))

    print("\nTokens:")
    print(tokens)

    tokens_sin_stopwords = eliminar_stopwords(tokens)

    print("\nSin stopwords:")
    print(tokens_sin_stopwords)

    tokens_stem = aplicar_stemming(tokens_sin_stopwords)

    print("\nCon stemming:")
    print(tokens_stem)

    print("\nResultado final:")
    print(preprocesar(ejemplo))