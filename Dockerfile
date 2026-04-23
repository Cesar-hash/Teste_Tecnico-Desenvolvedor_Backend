# 1. Usar uma imagem base oficial do Python
FROM python:3.12-slim

# 2. Definir o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copiar o arquivo de dependências primeiro (para otimizar o cache do Docker)
COPY requirements.txt .

# 4. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo o resto do código do projeto para o diretório de trabalho
COPY . .

# 6. Comando para iniciar a API quando o container for executado
#    Uvicorn irá rodar a aplicação 'app' que estará no arquivo 'api/main.py'
#    O host 0.0.0.0 é essencial para que a porta seja exposta para fora do container
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]