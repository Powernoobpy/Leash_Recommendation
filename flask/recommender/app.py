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

#Route
# @app.route('/recommendedPosts', methods=["GET"])
# @app.route('/recommendedPosts')
def recommendedPosts(user_id):
    print(user_id)
    try:
        # ---------------------now
        interactions = tuple(db.db.interactions.aggregate([
            {"$match":{"user_id":user_id}},
            {"$group": 
                {"_id": "$post_id",
                "interactions" : {"$sum":1}
            }
            }
        ]))
        # print(interactions)
        for item in interactions:
            item['user_id'] = user_id
            # tags = type(db.db.posts.find_one({"post_id":item['_id']}))
            # item['tags'] = tags
            # print(tags)
        
        # for x in interactions:
        #     print(x)
        # print(interactions)
        # posts = list(db.db.posts.find())
        # for user in interactions:
        #     user["_id"] = str(user["_id"])
        # for post in posts:
        #     post["_id"] = str(post["_id"])
        print(interactions)
        return interactions 
    #     return Response(
    #         response=json.dumps(interactions),
    #         status=200,
    #         mimetype="application/json")
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"errors":"cannot get any interaction"}),
            status=500,
            mimetype="application/json")

        # response = jsonify(interactions)
        # response.headers.add("Access-Control-Allow-Origin", "*")
        # print(response)
        # return response

        # return Response(
        # response=json.dumps(interactions),
        # status=200,
        # mimetype="application/json")

# @app.route('/posts', methods=["GET"])
def seeAllPosts():
    try:
        data = list(db.db.posts.find())
        for post in data:
            post["_id"] = str(post["_id"])
            # post["picture_link"] = list(post["picture_link"])
            post["tags"] = list(post["tags"])
            post['owner']['user_id'] = str(post['owner']['user_id'])
            # print(type(post["_id"]))
            # print(post["owner"]['user_id'])
        # print(data)
        return data
    #     return Response(
    #         response=json.dumps(data),
    #         status=200,
    #         mimetype="application/json")
    except Exception as ex:
        print(ex)
        # return Response(
        #     response=json.dumps({"errors":"cannot get posts"}),
        #     status=500,
        #     mimetype="application/json")
    return "flask mongodb atlas!"

#export
@app.route('/recommendedPosts', methods=["GET"])
def recommendation():
    try:
        user_id = request.args.get('user_id')
        # print(tuple(recommendedPosts(user_id)))
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
