FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y ffmpeg && apt-get install -y git && pip install --upgrade pip &&pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]

