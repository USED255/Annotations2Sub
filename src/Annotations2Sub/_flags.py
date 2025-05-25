# -*- coding: utf-8 -*-
"""Provides a simple global flags manager for the application.

This module defines a `flags` class and a global instance `Flags`
that can be used to store and access global application settings or
states, such as verbosity level.
"""


class flags:
    def __init__(self):
        self.verbose = False


Flags = flags()
