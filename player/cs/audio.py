# -*- coding: utf-8 -*-
import spotify
import logging
from collections import deque

from asyncio import coroutine, sleep, get_event_loop, async
from . import serializers

logging.basicConfig(level=logging.CRITICAL)

class Spotify(object):

    TRACK_ADDED = "sound.on_track_added"
    STATUS = "sound.status"

    def __init__(self, component):
        self.loop = get_event_loop()
        self.component = component
        self.queue = deque()
        self.track = None
        self.session = spotify.Session()
        self.player = self.session.player
        loop = spotify.EventLoop(self.session)
        self.audio = spotify.AlsaSink(self.session)
        loop.start()
        self.session.on(
            spotify.SessionEvent.END_OF_TRACK,
            self.on_track_ends
        )

    @property
    def logger(self):
        logger = logging.getLogger('common-sound')
        logger.setLevel(logging.INFO)
        return logger

    def on_track_ends(self, session):
        self.logger.info("track ended")
        self.track = None
        self.next_tune()

    def next_tune(self):
        if len(self.queue) > 0:
            self.queue.rotate(-1)
        track = self.queue[0]
        self.logger.info("add {} to event loop".format(track.name))
        self.loop.call_soon_threadsafe(async, self.play(track.link.uri))

    def login(self, user, password):
        self.session.login(user, password)

    @coroutine
    def find(self, q):
        results = self.session.search(q)
        while results.is_loaded is False:
            yield from sleep(1)
        response = {
            "state": self.player.state,
            "did_you_mean": results.did_you_mean,
            "artists": [],
            "tracks": [],
            "albums": []
        }
        for t in results.tracks:
            track = serializers.Track(t)
            response['tracks'].append(track.data)
        for a in results.artists:
            artist = serializers.Artist(a)
            response['artists'].append(artist.data)
        for a in results.albums:
            album = serializers.Album(a)
            response['albums'].append(album.data)
        return response

    @coroutine
    def play(self, uri):
        track = self.session.get_track(uri)
        while track.is_loaded is False:
            yield from sleep(1)
        self.track = track
        self.logger.info("playing {}".format(track.name))
        self.player.load(track)
        self.player.play()
        return self.status

    @coroutine
    def cover_image(self, uri):
        image = self.session.get_image(uri)
        while image.is_loaded is False:
            yield from sleep(1)
        return serializers.Image(image).data

    def pause(self):
        self.player.pause()
        return self.status

    def enqueue(self, uri):
        track = self.session.get_track(uri)
        while track.is_loaded is False:
            yield from sleep(1)

        self.queue.append(track)
        if self.player.state != spotify.PlayerState.PLAYING:
            self.logger.info("not playing so play straight away")
            self.next_tune()
        else:
            self.logger.info("playing so lets enqueue")
        return self.status

    @property
    def play_list(self):
        play_list = []
        for track in list(self.queue)[0:5]:
            t = serializers.Track(track)
            play_list.append(t.data)
        return play_list

    @property
    def status(self):
        state = {
            "state": self.player.state,
            "track": None,
            "next": None,
            "play_list": self.play_list
        }
        if self.track is not None:
            t = serializers.Track(self.track)
            state['track'] = t.data

        if len(self.queue) > 1:
            n = serializers.Track(self.queue[1])
            state['next'] = n.data
        return state

    def emit_status(self):
        self.logger.info("emitting status")
        self.component.publish(self.STATUS, self.status)
        yield from sleep(5)
        self.loop.call_soon_threadsafe(async, self.emit_status())