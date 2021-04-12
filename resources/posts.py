import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user # need to import for login credential requirements

post = Blueprint('posts', 'post')

# test routes with postman using --> localhost:8000/api/v1/posts/

@post.route('/', methods = ["GET"])
@login_required
def get_all_posts():
    try:
        posts = [model_to_dict(post) for post in models.Post.select()]
        print(posts)
        return jsonify(data=posts, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@post.route('/', methods = ["POST"])
def create_post():
    payload = request.get_json()
    payload['posted_by'] = current_user.id
    print(type(payload), 'payload')
    post = models.Post.create(**payload)
    post_dict = model_to_dict(post)
    return jsonify(data=post_dict, status={"code": 201, "message": "Success"})
    
