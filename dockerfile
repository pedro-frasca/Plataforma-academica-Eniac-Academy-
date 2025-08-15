# Usar uma imagem base com Python 3.12 e Alpine
FROM python:3.12-slim

# Configurar diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto
COPY . /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    default-libmysqlclient-dev \
    gfortran \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*
    
 

# Atualizar o pip
RUN pip install --no-cache-dir --upgrade pip

# Copiar e instalar as dependências do projeto
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt




# Expor a porta do Gunicorn
EXPOSE 8090

# Comando para rodar o Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8090", "AOEP.wsgi:application"]
