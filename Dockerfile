FROM python:3.11.5

RUN apt-get update && apt-get install -y libgl1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project including .env
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
