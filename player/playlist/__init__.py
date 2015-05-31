# -*- coding: utf-8 -*-
from mu.apps import AppConfig
from .sessions import PlaylistSession


class PlaylistConfig(AppConfig):
    name = "Playlist"
    label = "playlist"
    session_class = PlaylistSession


config = PlaylistConfig()
