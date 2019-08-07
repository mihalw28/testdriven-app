# base image
FROM python:3.7.4-slim

# install netcat
RUN apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

# set working directory
WORKDIR /usr/src/app

# add and install requirements
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/app

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh


# add app
# COPY . /usr/src/app

# run server
# CMD ["chmod","+x","/usr/src/app/entrypoint.sh"]
CMD ["/usr/src/app/entrypoint.sh"]
# CMD with "chmod" "+x" runs only in travis-ci, without doesn't run
# CMD just with path to entrypoint runs just local/docker-machine, doesn't run on travis-ci
# Wonder what to do.
