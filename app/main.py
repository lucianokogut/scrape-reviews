import os
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob
import logging

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho para o arquivo de avaliações
file_path = os.path.join('app', 'data', 'avaliacoes.text')

# 1. Coleta de Dados
def scrape_reviews_from_file(file_path):
    logging.info(f'Iniciando a coleta de avaliações do arquivo: {file_path}')
    with open(file_path, 'r', encoding='utf-8') as file:
        reviews = file.readlines()
    logging.info(f'Foram coletadas {len(reviews)} avaliações do arquivo')
    return reviews

reviews = scrape_reviews_from_file(file_path)

# 2. Pré-processamento
def preprocess_reviews(reviews):
    logging.info('Iniciando pré-processamento das avaliações')
    cleaned_reviews = []
    stop_words = set(stopwords.words('portuguese'))
    lemmatizer = WordNetLemmatizer()

    for review in reviews:
        # Remove caracteres especiais e converte para minúsculas
        cleaned_text = ''.join(e for e in review if e.isalnum() or e.isspace()).lower()
        
        # Tokenização
        words = word_tokenize(cleaned_text)

        # Remoção de stop words e lematização
        cleaned_words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]

        cleaned_reviews.append(cleaned_words)

    logging.info('Pré-processamento das avaliações concluído')
    return cleaned_reviews

cleaned_reviews = preprocess_reviews(reviews)

# 3. Análise de Sentimento
def analyze_sentiment(review):
    logging.info('Iniciando análise de sentimento')
    blob = TextBlob(review)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return 'positivo'
    elif sentiment_score < 0:
        return 'negativo'
    else:
        return 'neutro'

sentiments = [analyze_sentiment(' '.join(review)) for review in cleaned_reviews]

# 4. Geração da Nuvem de Palavras
def generate_wordcloud(words, sentiments):
    logging.info('Gerando nuvem de palavras')
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(words)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

def generate_word_frequencies(reviews, sentiments):
    logging.info('Gerando frequências de palavras')
    word_frequencies = {}
    for review, sentiment in zip(reviews, sentiments):
        for word in review:
            if word not in word_frequencies:
                word_frequencies[word] = {'positivo': 0, 'negativo': 0, 'neutro': 0}
            word_frequencies[word][sentiment] += 1
    logging.info('Frequências de palavras geradas')
    return word_frequencies

word_frequencies = generate_word_frequencies(cleaned_reviews, sentiments)

# Exemplo de visualização da nuvem de palavras para palavras predominantemente positivas
positive_words = {word: freq['positivo'] for word, freq in word_frequencies.items()}
generate_wordcloud(positive_words, sentiments)
