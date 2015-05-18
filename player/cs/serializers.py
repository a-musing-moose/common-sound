# -*- coding: utf-8 -*-


class Serializer(object):

    def __init__(self, obj):
        self.obj = obj

    def get_context_data(self):
        return {}

    @property
    def data(self):
        data = self.get_context_data()
        data['uri'] = self.obj.link.uri
        return data


class Artist(Serializer):

    def get_context_data(self):
        return {'name': self.obj.name}


class Track(Serializer):

    def get_context_data(self):
        artists = []
        for artist in self.obj.artists:
            s = Artist(artist)
            artists.append(s.data)
        return {
            "name": self.obj.name,
            "artists": artists,
            "duration": self.obj.duration
        }


class Album(Serializer):
    def get_context_data(self):
        artist = Artist(self.obj.artist)
        return {
            "name": self.obj.name,
            "artists": artist.data,
            "cover_uri": self.obj.cover_link().uri
        }


class Image(Serializer):
    def get_context_data(self):
        return {
            "type": self.obj.format,
            "data": self.obj.data_uri
        }
