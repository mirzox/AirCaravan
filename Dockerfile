FROM python:3.11
WORKDIR /app
COPY requirements.txt .
COPY . .
RUN pip3 install -r requirements.txt
