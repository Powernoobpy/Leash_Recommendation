from flask import Flask
from flask_pymongo import pymongo
from app import app

CONNECTION_STRING = "mongodb+srv://leashposts:leashmasterposts@leash.t5u93.mongodb.net/Leash?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database("Leash")
# user_collection = pymongo.collection.Collection(db, 'users')
# post_collection = pymongo.collection.Collection(db, 'posts')