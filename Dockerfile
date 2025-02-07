# Używamy obrazu Pythona
FROM python:3.10

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy pliki projektu
COPY . .

# Instalujemy wymagane pakiety
RUN pip install --no-cache-dir psycopg2-binary flask

# Uruchamiamy aplikację webową Flask
CMD ["python", "app.py"]
