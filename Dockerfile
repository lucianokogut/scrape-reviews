# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY ./app/requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código-fonte para o diretório de trabalho
COPY ./app .

# Comando padrão a ser executado quando o contêiner for iniciado
CMD ["python", "main.py"]
