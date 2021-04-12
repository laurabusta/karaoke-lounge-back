import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
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
        # profile = models.Profile.create(**payload) # put the user in the database
        profile = models.Profile.create(**payload)
        # starts user session
        login_user(profile)
        profile_dict = model_to_dict(profile) # puts user model into dictionary format
        # delete the password before we return it, because we don't need the client to be aware of it
        print(profile_dict)
        print(type(profile_dict))
        del profile_dict['password']

        return jsonify(data=profile_dict, status={"code": 201, "message": "Success"})

@profile.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print('payload:', payload)
    payload['email'] = payload['email'].lower() # make lower case

    try:
        profile = models.Profile.get(models.Profile.email == payload['email']) # Try to find the user by their email
        profile_dict = model_to_dict(profile) # if you find the User model convert in to a dictionary so you can edit and jsonify it
        if(check_password_hash(profile_dict['password'], payload['password'])): # use bcrypt to check password and see if input password matches
            del profile_dict['password'] # delete the password since the client doesn't need it
            login_user(profile) # set up the session
            print(profile, ' this is user profile')
            login_response = jsonify(data=profile_dict, status={"code": 200, "message": "Success"})
            print(login_response)
            return login_response # respond to the client
        else:
            return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@profile.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    print(current_user.__dict__)
    return jsonify(data={}, status={"code": 200, "message": "Successful log out"})

@profile.route('/', methods=["GET"])
@login_required
def get_all_profiles():
    try:
        profiles = [model_to_dict(profile) for profile in models.Profile.select()]
        print(profiles)
        return jsonify(data=profiles, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@profile.route('/<profile_id>', methods=["PUT"])
@login_required
def update_profile(profile_id):
    try:
        payload = request.get_json()
        query = models.Profile.update(**payload).where(models.Profile.id==profile_id)
        query.execute()
        profile = models.Profile.get_by_id(profile_id)
        return jsonify(data=model_to_dict(profile), status={"code": 200, "message": "resource updated successfully"})
    except AttributeError:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@profile.route('/<profile_id>', methods=["DELETE"])
@login_required
def delete_profile(profile_id):
    query = models.Profile.delete().where(models.Profile.id==profile_id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})