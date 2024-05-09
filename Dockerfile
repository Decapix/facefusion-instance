# Utilise une image de base officielle Python
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
COPY requirement_facefusion_and_controller.txt requirement_facefusion_and_controller.txt
RUN pip install --no-cache-dir -r requirement_facefusion_and_controller.txt

COPY . .

# Commande pour lancer l'application
CMD ["uvicorn", "controller2.main:app", "--host", "0.0.0.0", "--port", "80"]
