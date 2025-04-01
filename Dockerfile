FROM python:3.11.5

RUN apt-get update && apt-get install -y libgl1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["fastapi", "dev", "app/main.py", "--port", "8000"]
