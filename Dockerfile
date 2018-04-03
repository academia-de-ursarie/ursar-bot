FROM python:3-alpine

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD [ "python", "ursar.py" ]