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


class Spotify(object):

    PLAYLIST = "sound.new_playlist"
    STATUS = "sound.status"

    def __init__(self, component):
        self.loop = get_event_loop()
        self.component = component
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
        self.loop.call_soon_threadsafe(async, self.next_tune())
        self.next_tune()

    @coroutine
    def next_tune(self):
        track = yield from self.component.call("playlist.next")
        if track:
            self.loop.call_soon_threadsafe(async, self.play(track))

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
    def top_tracks(self, region='AU'):
        top_tracks = self.session.get_toplist(
            spotify.ToplistType.TRACKS,
            region=region
        )
        while top_tracks.is_loaded is False:
            yield from sleep(0.1)
        tracks = []
        for track in top_tracks.tracks:
            t = serializers.Track(track)
            tracks.append(t.data)
        return tracks

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
        track = self.session.get_track(uri)
        while track.is_loaded is False:
            yield from sleep(0.1)

        yield from self.component.call(
            "playlist.add",
            session_id,
            track.link.uri
        )
        if self.player.state != spotify.PlayerState.PLAYING:
            self.logger.info("not playing so play straight away")
            yield from self.next_tune()
        else:
            self.logger.info("playing so lets enqueue")
        yield from self.emit_playlist()
        return self.status

    @coroutine
    def vote_up(self, uri, session_id):
        yield from self.component.call("playlist.vote_up", uri, session_id)
        yield from self.emit_playlist()
        return self.status

    @coroutine
    def vote_down(self, uri, session_id):
        yield from self.component.call("playlist.vote_down", uri, session_id)
        yield from self.emit_playlist()
        tracks = yield from self.component.call("playlist.get_all")
        if uri not in tracks:
            yield from self.next_tune()
        return self.status

    @coroutine
    def playlist(self, *args, **kwargs):
        play_list = []
        tracks = yield from self.component.call("playlist.get_all")
        for uri in tracks:
            track = self.session.get_track(uri)
            while track.is_loaded is False:
                yield from sleep(0.1)
            t = serializers.Track(track)
            play_list.append(t.data)
        return play_list

    @property
    def status(self):
        state = {
            "state": self.player.state,
            "track": None
        }
        if self.track is not None:
            t = serializers.Track(self.track)
            state['track'] = t.data
        return state

    def emit_playlist(self):
        play_list = yield from self.playlist()
        self.component.publish(self.PLAYLIST, play_list)

    @coroutine
    def emit_status(self):
        self.logger.info("emitting status")
        self.component.publish(self.STATUS, self.status)
        self.loop.call_later(5, async, self.emit_status())
