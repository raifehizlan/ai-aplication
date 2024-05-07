FROM python:3.8-slim
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt
WORKDIR /app
COPY . /app
EXPOSE 80
CMD ["python3", "app.py"]