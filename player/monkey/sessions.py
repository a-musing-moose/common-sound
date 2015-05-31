# -*- coding: utf-8 -*-
from asyncio import coroutine, get_event_loop, async
from random import randint, choice
from autobahn.asyncio.wamp import ApplicationSession
from datetime import datetime, timedelta


class MonkeySession(ApplicationSession):

    @coroutine
    def how_bout_dis(self):
        if self.enabled:
            print("Musical monkey magic...")
            try:
                top_tracks = yield from self.call("sound.top_tracks")
            except:
                top_tracks = []
            if len(top_tracks) > 0:
                track = choice(top_tracks)
                print("Adding {}".format(track['name']))
                yield from self.call(
                    "sound.enqueue",
                    track['uri'],
                    "monkey_magic"
                )
        else:
            print("no magic")
        delay = randint(300, 900)
        diff = timedelta(seconds=delay)
        n = datetime.now() + diff
        print("more magic at {}".format(n.strftime("%H:%M:%S")))
        self.loop.call_later(delay, async, self.how_bout_dis())

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def onJoin(self, details):
        print("music monkey connected")
        self.loop = get_event_loop()
        self.enabled = True
        yield from self.register(self.enable, "monkey.enable")
        yield from self.register(self.disable, "monkey.disable")
        yield from self.how_bout_dis()
