FROM python:3.10-slim-buster

WORKDIR /app

RUN apt-get update

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .

ENTRYPOINT [ "python" ]
CMD ["run.py" ]