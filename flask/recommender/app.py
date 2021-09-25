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

#Route
@app.route('/recommendedPosts', methods=["GET"])
def recommendedPosts():
    # try:
        user_id = request.args.get('user_id')
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
            # tags = type(db.db.posts.find_one({"post_id":item['_id']}))
            # item['tags'] = tags
            # print(tags)
        # print(interactions)
        # posts = list(db.db.posts.find())
        # for user in interactions:
        #     user["_id"] = str(user["_id"])
        # for post in posts:
        #     post["_id"] = str(post["_id"])
        
    #     return Response(
    #         response=json.dumps(interactions),
    #         status=200,
    #         mimetype="application/json")
    # except Exception as ex:
    #     print(ex)
    #     return Response(
    #         response=json.dumps({"errors":"cannot get any interaction"}),
    #         status=500,
    #         mimetype="application/json")
        response = jsonify(interactions)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        # return Response(
        # response=json.dumps(interactions),
        # status=200,
        # mimetype="application/json")

@app.route('/posts', methods=["GET"])
def seeAllPosts():
    try:
        data = list(db.db.posts.find())
        for post in data:
            post["_id"] = str(post["_id"])
            post["picture_link"] = list(post["picture_link"])
            post["tags"] = list(post["tags"])
            for user in post["owner"]:
                user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"errors":"cannot get posts"}),
            status=500,
            mimetype="application/json")
    return "flask mongodb atlas!"

#export
if __name__ == '__main__':
    app.run(port=5000, debug=True)