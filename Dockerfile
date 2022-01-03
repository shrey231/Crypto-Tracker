FROM python:3.9.5

RUN apt-get update

RUN apt-get -y install cron 

COPY . .

RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["cron", "-f"]
