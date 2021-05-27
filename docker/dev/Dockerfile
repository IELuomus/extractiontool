FROM python:3
ENV WORKER_COUNT=2
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get update && apt install -y openjdk-11-jre-headless imagemagick python3-opencv mariadb-client setools ghostscript-x tesseract-ocr
RUN export JAVA_HOME
RUN sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="none" pattern="OHTU_PROJEKTI_DISABLED_PDF" \/>/'  "/etc/ImageMagick-6/policy.xml"
COPY --chown=root . /code/
#RUN chmod -R 777 /code
ENTRYPOINT ["/bin/bash", "./docker/dev/docker-entrypoint-dev.sh"]
