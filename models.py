from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = PostgresqlDatabase('karaoke')

class Profile(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    nickname = CharField()
    fave_drink = CharField()
    fave_genre = CharField()
    profile_pic_URL = CharField()

    class Meta:
        database = DATABASE

class Song(Model):
    title = CharField()
    artist = CharField()
    genre = CharField()
    image = CharField()
    song_code = CharField()
    music_brainz_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    posted_by = ForeignKeyField(Profile, backref='profiles')

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Profile, Song], safe=True)
    print("TABLES Created")
    DATABASE.close()