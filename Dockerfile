FROM python:3.11

RUN apt-get update

# copy code
WORKDIR /code
RUN touch /code/.git
COPY ./requirements.txt /code/requirements.txt

# install 
RUN sudo pip3 install -r requirements.txt

# run FastAPI
COPY ./app /code/app
COPY ./scripts /code/scripts
RUN sudo chmod +x /code/scripts/run.sh

ENTRYPOINT ["sh", "./scripts/run.sh"]