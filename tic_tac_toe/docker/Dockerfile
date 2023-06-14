# syntax=docker/dockerfile:1.4

FROM python:3.10
EXPOSE 5000
EXPOSE 8000
EXPOSE 5432
WORKDIR /app
COPY requirements.txt /app
COPY run.sh /run.sh
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["/bin/bash", "/run.sh"]