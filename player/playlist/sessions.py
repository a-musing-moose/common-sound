# -*- coding: utf-8 -*-
import yaml
from autobahn.asyncio.wamp import ApplicationSession
from .ordering import confidence


class Playlist(object):

    MAX_POOPS = 3

    def __init__(self, path=None):
        self.index = 0
        self.playlist = []
        self.path = path
        self._load()

    def _load(self):
        try:
            with open(self.path, "r") as f:
                self.playlist = yaml.safe_load(f)
        except:
            pass

    def _save(self):
        with open(self.path, "w") as f:
            f.write(yaml.dump(self.playlist))

    def _get_track(self, uri):
        for track in self.playlist:
            if uri == track['uri']:
                return track
        return None

    def add_track(self, session_id, uri):
        track = self._get_track(uri)
        if track:
            self.vote_up(uri, session_id)
            return
        self.playlist.append({
            "uri": uri,
            "up": [
                session_id,
            ],
            "down": []
        })
        self._save()

    def remove_track(self, uri):
        track = self._get_track(uri)
        if track:
            self.playlist.remove(track)
            self._save()
        return

    def next_track(self):
        if len(self.playlist) > 0:
            self.index += 1
            if self.index >= len(self.playlist):
                self.full_sort()
                self.index = 0
            return self.playlist[self.index]["uri"]
        return None

    def vote_up(self, uri, session_id):
        track = self._get_track(uri)
        if track and session_id not in track['up']:
            track["up"].append(session_id)
        self.partial_sort()
        self._save()

    def vote_down(self, uri, session_id):
        track = self._get_track(uri)
        if track and session_id not in track['down']:
            track['down'].append(session_id)
            if len(track['down']) > self.MAX_POOPS:
                self.remove_track(uri)
            else:
                self.partial_sort()
        self._save()

    def _sort(self, items):
        items.sort(
            key=lambda t: confidence(len(t["up"]), len(t["down"])),
            reverse=True
        )
        return items

    def partial_sort(self):
        current = self.playlist[self.index]
        head = self.playlist[0:self.index]
        head = self._sort(head)
        tail = self.playlist[self.index+1:]
        tail = self._sort(tail)
        self.playlist = head + [current] + tail

    def full_sort(self):
        self.playlist = self._sort(self.playlist)

    def __iter__(self):
        data = [d["uri"] for d in self.playlist]
        return data.__iter__()

    def __getitem__(self, key):
        return self.playlist[key]["uri"]

    def __len__(self):
        return len(self.playlist)


class PlaylistSession(ApplicationSession):

    def get_all(self):
        tracks = [t for t in self.playlist]
        return tracks

    def onJoin(self, details):
        print("playlist connected")
        playlist_file = self.config.extra.playlist
        print("loading playlist from {}".format(playlist_file))
        self.playlist = Playlist(playlist_file)
        yield from self.register(self.playlist.vote_up, 'playlist.vote_up')
        yield from self.register(self.playlist.vote_down, 'playlist.vote_down')
        yield from self.register(self.playlist.add_track, 'playlist.add')
        yield from self.register(self.playlist.next_track, 'playlist.next')
        yield from self.register(self.playlist.__getitem__, 'playlist.get')
        yield from self.register(self.get_all, 'playlist.get_all')
