FROM python:3.8.10

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r recommender/requirements.txt

EXPOSE 5000
CMD [ "python3", "app.py", "5000" ]