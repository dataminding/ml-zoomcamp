FROM agrigorev/zoomcamp-model:3.8.12-slim

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pip install pipenv
RUN pipenv install --system

COPY churn.py ./

EXPOSE 9222

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9222", "churn:app"]