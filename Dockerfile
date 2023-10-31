FROM python:3.11.1

WORKDIR /code

# copy code
COPY ./requirements.txt /code/requirements.txt

# install 
RUN pip install --no-cache-dir -r /code/requirements.txt

# run FastAPI
COPY ./app /code/app
COPY ./scripts /code/scripts
RUN chmod +x /code/scripts/run.sh

ENTRYPOINT ["./scripts/run.sh"]