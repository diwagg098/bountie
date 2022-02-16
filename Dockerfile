FROM python:3.9

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

RUN ln /usr/local/bin/python3.9 /usr/bin/python

EXPOSE 8000
# ENTRYPOINT [ "NEW_RELIC_CONFIG_FILE=/app/newrelic.ini", "newrelic-admin", "run-program" ]
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

