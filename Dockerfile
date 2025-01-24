FROM python:3.12.4

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
