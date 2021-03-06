# python:alpine is 3.{latest}
FROM python:2.7-alpine 

RUN pip install flask ; \
    pip install xmltodict

COPY app.py /app/
COPY static /app/
COPY templates /app/

EXPOSE 5000

ENV FLASK_APP=/app/app.py

ENTRYPOINT ["flask", "run"]
