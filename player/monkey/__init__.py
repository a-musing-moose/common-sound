# -*- coding: utf-8 -*-
from mu.apps import AppConfig
from .sessions import MonkeySession


class MonkeyConfig(AppConfig):
    name = "Music Monkey"
    label = "music-monkey"
    session_class = MonkeySession


config = MonkeyConfig()
