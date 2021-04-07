import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

profile = Blueprint('profiles', 'profile') # do I need the url_prefix?

@profile.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    print(payload)

    try:
        models.Profile.get(models.Profile.email == payload['email'])

        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        profile = models.Profile.create(**payload) # put the user in the database
        # starts user session
        login_user(profile)
        profile_dict = model_to_dict(profile) # puts user model into dictionary format
        # delete the password before we return it, because we don't need the client to be aware of it
        print(profile_dict)
        print(type(profile_dict))
        del profile_dict['password']

        return jsonify(data=profile_dict, status={"code": 201, "message": "Success"})

