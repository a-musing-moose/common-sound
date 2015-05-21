# -*- coding: utf-8 -*-
import sys
import spotify
import logging

from asyncio import coroutine, sleep, get_event_loop, async
from spotify.sink import Sink

from . import serializers

logging.basicConfig(level=logging.CRITICAL)


class AlsaSink(Sink):

    def __init__(self, session, card=-1):
        self._session = session
        self._card = card

        import alsaaudio  # Crash early if not available
        self._alsaaudio = alsaaudio
        self._device = None

        self.on()

    def _on_music_delivery(self, session, audio_format, frames, num_frames):
        assert (
            audio_format.sample_type == spotify.SampleType.INT16_NATIVE_ENDIAN)

        if self._device is None:
            self._device = self._alsaaudio.PCM(
                mode=self._alsaaudio.PCM_NONBLOCK, cardindex=self._card)
            if sys.byteorder == 'little':
                self._device.setformat(self._alsaaudio.PCM_FORMAT_S16_LE)
            else:
                self._device.setformat(self._alsaaudio.PCM_FORMAT_S16_BE)
            self._device.setrate(audio_format.sample_rate)
            self._device.setchannels(audio_format.channels)
            self._device.setperiodsize(num_frames * audio_format.frame_size())

        return self._device.write(frames)

    def _close(self):
        if self._device is not None:
            self._device.close()
            self._device = None


class Playlist(object):

    def __init__(self):
        self.index = 0
        self.playlist = []

    def add_track(self, session_id, track):
        self.playlist.append({
            "track": track,
            "votes": [
                session_id,
            ],
            "poop": 0
        })

    def next_track(self):
        if len(self.playlist) > 0:
            self.index += 1
            if self.index >= len(self.playlist):
                self.index = 0
            return self.playlist[self.index]["track"]
        return None

    def add_vote(self, uri, session_id):
        for entry in self.playlist:
            entry_uri = entry["track"].link.uri
            if uri == entry_uri and session_id not in entry['votes']:
                entry["votes"].append(session_id)
        self.sort()

    def sort(self):
        current = self.playlist.pop(self.index)
        remainder = self.playlist[0:self.index] + self.playlist[self.index:]
        remainder.sort(key=lambda t: len(t["votes"]), reverse=True)
        self.playlist = [current] + remainder
        self.index = 0

    def __iter__(self):
        data = [d["track"] for d in self.playlist]
        return data.__iter__()

    def __getitem__(self, key):
        return self.playlist[key]["track"]

    def __len__(self):
        return len(self.playlist)


class Spotify(object):

    PLAYLIST = "sound.new_playlist"
    STATUS = "sound.status"

    def __init__(self, component):
        self.loop = get_event_loop()
        self.component = component
        self.queue = Playlist()
        self.track = None
        self.session = spotify.Session()
        self.player = self.session.player
        loop = spotify.EventLoop(self.session)
        self.audio = AlsaSink(self.session)
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
        track = self.queue.next_track()
        if track:
            self.logger.info("add {} to event loop".format(track.name))
            self.loop.call_soon_threadsafe(async, self.play(track.link.uri))

    def login(self, user, password):
        self.session.login(user, password)

    @coroutine
    def find(self, q):
        results = self.session.search(q)
        while results.is_loaded is False:
            yield from sleep(0.1)
        response = {
            "state": self.player.state,
            "did_you_mean": results.did_you_mean,
            "artists": [],
            "artist_total": results.artist_total,
            "tracks": [],
            "track_total": results.track_total,
            "albums": [],
            "album_total": results.album_total
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
            yield from sleep(0.1)
        self.track = track
        self.logger.info("playing {}".format(track.name))
        self.player.load(track)
        self.player.play()
        return self.status

    @coroutine
    def cover_image(self, uri):
        image = self.session.get_image(uri)
        while image.is_loaded is False:
            yield from sleep(0.1)
        return serializers.Image(image).data

    def pause(self):
        if self.player.state == spotify.PlayerState.PLAYING:
            self.player.pause()
        elif self.player.state == spotify.PlayerState.PAUSED:
            self.player.play()
        return self.status

    @coroutine
    def enqueue(self, uri, session_id):
        self.logger.info("session: {}".format(session_id))
        track = self.session.get_track(uri)
        while track.is_loaded is False:
            yield from sleep(0.1)

        self.queue.add_track(session_id, track)
        if self.player.state != spotify.PlayerState.PLAYING:
            self.logger.info("not playing so play straight away")
            self.next_tune()
        else:
            self.logger.info("playing so lets enqueue")
        self.component.publish(self.PLAYLIST, self.playlist())
        return self.status

    def vote(self, uri, session_id):
        self.queue.add_vote(uri, session_id)
        self.component.publish(self.PLAYLIST, self.playlist())
        return self.status

    def playlist(self, *args, **kwargs):
        play_list = []
        for track in self.queue:
            t = serializers.Track(track)
            play_list.append(t.data)
        return play_list

    @property
    def status(self):
        state = {
            "state": self.player.state,
            "track": None,
            "next": None
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
