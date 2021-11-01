FROM python:3.9.7-slim

RUN mkdir /app

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pip install pipenv
RUN pipenv install --system

COPY models/ models/
COPY predict_bikerental.py ./

EXPOSE 9911

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9911", "predict_bikerental:app"]