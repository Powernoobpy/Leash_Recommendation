from flask import Flask
from flask.wrappers import Response
import json
from bson.objectid import ObjectId
app = Flask(__name__)
import db

try:
    print("db conected")
except:
    print("cannote connect to db")

#Route
@app.route('/posts', methods=["GET"])
def seeAllPosts():
    try:
        data = list(db.db.posts.find())
        for user in data:
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