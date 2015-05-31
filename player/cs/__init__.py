# -*- coding: utf-8 -*-
from mu.apps import AppConfig
from .sessions import CommonSound


class PlayerConfig(AppConfig):
    name = "Common Sound"
    label = "common-sound"
    session_class = CommonSound


config = PlayerConfig()
