FROM python:3.8.10

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "/usr/src/app/app.py", "5000" ]