#!/usr/bin/env python

import time
import logging
import random
import Queue

import hollywood
import hollywood.actor

import meter


class Registry(object):
    """
        Spawn an actor for each subclass of poller.Base.

        Store that ActorRef so we can .ask() it for new
        data obtained from polling.
    """

    pollers = {}
    futures = []
    last_response = {}

    @classmethod
    def register(cls, actor, params):
        hollywood.System.register(actor)
        poller = hollywood.System.new(actor.address[0])
        cls.pollers[poller] = params
        cls.futures.append(poller.ask(params))

    @classmethod
    def get(cls):
        """
            Checks for each future to see if it's ready for all actors.
            If true, replaces the buffered response with the new one and
            creates a new future (actor.ask()).

            The response of all actors (some may be fresh, others may be
            buffered from previous iterations) is returned.
        """
        for idx, p in enumerate(cls.pollers.keys()):
            if cls.futures[idx].empty():
                continue
            cls.last_response[idx] = cls.futures[idx].get()
            cls.futures[idx] = p.ask(cls.pollers[p])
        return '\n'.join(cls.last_response.values())
