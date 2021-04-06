from peewee import *
import datetime

DATABASE = PostgresqlDatabase('karaoke')

class Song(Model):
    title = CharField()
    artist = CharField()
    genre = CharField()
    image = CharField()
    song_code = CharField()
    music_brainz_id = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Song], safe=True)
    print("TABLES Created")
    DATABASE.close()