# -*- coding: utf-8 -*-
from autobahn.asyncio.wamp import ApplicationSession
from .audio import Spotify


class CommonSound(ApplicationSession):

    def _spotify_credentials(self):
        return {
            "user": self.config.extra.spotify_user,
            "password": self.config.extra.spotify_password,
        }

    def onJoin(self, details):
        print("Joined realm: {0}, session id: {1}".format(
            details.realm,
            details.session
        ))
        self.spotify = Spotify(self)
        creds = self._spotify_credentials()
        self.spotify.login(creds['user'], creds['password'])
        yield from self.register(self.spotify.find, 'sound.find')
        yield from self.register(self.spotify.play, 'sound.play')
        yield from self.register(self.spotify.pause, 'sound.pause')
        yield from self.register(self.spotify.cover_image, 'sound.cover_image')
        yield from self.register(self.spotify.enqueue, 'sound.enqueue')
        yield from self.register(self.spotify.playlist, 'sound.playlist')
        yield from self.register(self.spotify.vote, 'sound.vote')
        yield from self.spotify.emit_status()
