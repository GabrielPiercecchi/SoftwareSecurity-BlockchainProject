FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#CMD ["python", "app.py"]

CMD ["gunicorn", "--config", "config/gunicorn/gunicorn.conf.py", "app:app"]
