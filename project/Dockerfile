FROM python:latest

WORKDIR /usr/src/app/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get -y update
RUN apt-get install -y python  gcc python3-dev musl-dev


COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY ./wait-for-postgres.sh .
RUN chmod +x /usr/src/app/wait-for-postgres.sh


COPY . /usr/src/app/

RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install -r requirements.txt


ENTRYPOINT ["/usr/src/app/entrypoint.sh"]