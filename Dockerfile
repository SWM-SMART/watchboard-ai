FROM python:3.11

RUN apt-get update

# copy code
WORKDIR /code
RUN touch ./.git
COPY ./requirements.txt ./requirements.txt

# install 
RUN pip3 install -r requirements.txt

# run FastAPI
COPY ./app ./app
COPY ./scripts ./scripts
RUN chmod +x ./scripts/run.sh

ENTRYPOINT ["./scripts/run.sh"]