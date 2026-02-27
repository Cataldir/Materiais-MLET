# Dockerfile — imagem Python para aplicação de ML
# Build: docker build -t ml-app .
# Run: docker run -p 8000:8000 ml-app

FROM python:3.12-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY app.py .

# Cria usuário não-root para segurança
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Expõe porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Comando de inicialização
CMD ["python", "app.py"]
