FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt && \
    python -m spacy download en_core_web_sm

COPY . /app

EXPOSE 8005

CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]