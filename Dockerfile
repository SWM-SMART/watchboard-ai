FROM python:3.10

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app
COPY ./scripts /code/scripts
RUN chmod +x /code/scripts/run.sh

ENTRYPOINT ["./scripts/run.sh"]