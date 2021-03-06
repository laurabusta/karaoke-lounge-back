import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import login_required, current_user # need to import for login credential requirements

song = Blueprint('songs', 'song')

# test routes with postman using --> localhost:8000/api/v1/songs/

@song.route('/', methods=["GET"])
@login_required # added this line to require login credentials to use route
def get_all_songs():
    ## find the songs and change each one to a dictionary into a new array
    try:
        songs = [model_to_dict(song) for song in models.Song.select()]
        print(songs)
        return jsonify(data=songs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@song.route('/user/<user_id>', methods=["GET"])
def get_songs_by_user(user_id):
    try:
        songs = [model_to_dict(song) for song in models.Song.select().join(models.Profile).where(models.Profile.id == user_id)]
        print(songs)
        return jsonify(data=songs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

@song.route('/', methods=["POST"])
def create_songs():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    payload['posted_by'] = current_user.id
    print(type(payload), 'payload')
    song = models.Song.create(**payload)
    ## see the object
    print(song.__dict__)
    ## Look at all the methods
    print(dir(song))
    # Change the model to a dict
    print(model_to_dict(song), 'model to dict')
    song_dict = model_to_dict(song)
    return jsonify(data=song_dict, status={"code": 201, "message": "Success"})

@song.route('/<song_id>', methods=["DELETE"])
def delete_song(song_id):
    query = models.Song.delete().where(models.Song.id==song_id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

@song.route('/<song_id>', methods=["PUT"])
def update_song(song_id):
    payload = request.get_json()
    query = models.Song.update(**payload).where(models.Song.id==song_id)
    query.execute()
    song = models.Song.get_by_id(song_id)
    return jsonify(data=model_to_dict(song), status={"code": 200, "message": "resource updated successfully"})

    
