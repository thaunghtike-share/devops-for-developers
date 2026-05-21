FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000
ENV APP_NAME="Hello Docker World"
CMD ["python", "app.py"]