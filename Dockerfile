FROM python:3.12-slim

# Arbeitsverzeichnis
WORKDIR /app

# Systemabhängigkeiten installieren (gcc, libffi, python-dev)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Abhängigkeiten kopieren
COPY requirements.txt .

# Python-Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Rest des Codes kopieren
COPY . .

# Bot starten
CMD ["python", "main.py"]

