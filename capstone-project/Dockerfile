FROM python:3.9.7-slim

RUN mkdir /app

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --system

COPY capstone_model.pickle capstone_transformer.pickle predict_fake_job.py ./

EXPOSE 9911

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9911", "predict_fake_job:app"]