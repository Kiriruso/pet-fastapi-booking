FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN rm -r ./app/tests/

RUN chmod a+x /booking/docker/*.sh