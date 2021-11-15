from array import array
from re import match
from flask import Flask, request, jsonify
import flask
from flask.wrappers import Response
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
from werkzeug.wrappers import response
app = Flask(__name__)
import db
from recommendation import lightfmReccomend

def recommendedPosts(user_id):
    print(user_id)
    try:
        interactions = tuple(db.db.interactions.aggregate([
            {"$match":{"user_id":user_id}},
            {"$group": 
                {"_id": "$post_id",
                "interactions" : {"$sum":1}
            }
            }
        ]))
        
        for item in interactions:
            item['user_id'] = user_id
  
        print(interactions)
        return interactions 

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"errors":"cannot get any interaction"}),
            status=500,
            mimetype="application/json")

# @app.route('/posts', methods=["GET"])
def seeAllPosts():
    try:
        data = list(db.db.posts.find())
        for post in data:
            post["_id"] = str(post["_id"])
            post["tags"] = list(post["tags"])
            if("_id" in post["owner"]):
                post["owner"]["_id"] = str(post["owner"]["_id"])
            if("user_id" in post["owner"]):
                post["owner"]["user_id"] = str(post["owner"]["user_id"])
        return data

    except Exception as ex:
        print(ex)
    return "flask mongodb atlas!"

#export
@app.route('/recommendedPosts', methods=["GET"])
def recommendation():
    try:
        user_id = request.args.get('user_id')
        recommend = lightfmReccomend(recommendedPosts(user_id),seeAllPosts())
        # print(recommend)
        return Response(
            response=json.dumps(recommend),
            status=200,
            mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"errors":"cannot get recommend posts"}),
            status=500,
            mimetype="application/json")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
