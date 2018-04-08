FROM python:3-alpine

WORKDIR /app
COPY . .
RUN apk add --no-cache tzdata \
  && cp /usr/share/zoneinfo/Europe/Bucharest /etc/localtime \
  && echo "Europe/Bucharest" > /etc/timezone \
  && pip install -r requirements.txt

CMD [ "python", "ursar.py" ]