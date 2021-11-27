FROM python:3.8.10-alpine

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python3", "app.py", "5000" ]