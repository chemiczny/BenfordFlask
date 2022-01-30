FROM alpine:3.13
WORKDIR /app/
FROM python:3.9-slim
COPY requirements.txt .
COPY benford ./benford

RUN pip3 install -r requirements.txt 
COPY wsgi.py .
CMD ["python3", "wsgi.py"]
