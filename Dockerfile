FROM python:3.9

COPY . ./app
WORKDIR ./app

RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]