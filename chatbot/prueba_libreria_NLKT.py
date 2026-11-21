import nltk

nltk.data.path.append(
    r"C:\Users\sesa724651\nltk_data"
)

from nltk.corpus import stopwords

print(stopwords.words("spanish")[:10])