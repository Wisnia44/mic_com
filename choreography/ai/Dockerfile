FROM python:3.10-slim

WORKDIR /code

RUN pip install --no-cache-dir --upgrade pipenv
COPY ../Pipfile .
COPY ../Pipfile.lock .
RUN pipenv install

COPY ./ai .

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
