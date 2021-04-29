FROM python:3
ENV WORKER_COUNT=2
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt install -y openjdk-11-jre-headless imagemagick python3-opencv mariadb-client
RUN export JAVA_HOME
COPY --chown=root . /code/
#RUN chmod -R 777 /code
ENTRYPOINT ["/bin/bash", "./docker-entrypoint-prod.sh"]
