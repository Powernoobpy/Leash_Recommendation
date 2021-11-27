FROM python:3.8.10-alpine

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r recommender/requirements.txt

EXPOSE 5000
CMD [ "python3", "recommender/app.py" ]