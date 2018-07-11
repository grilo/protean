#!/usr/bin/env python

"""
    Traverse all registered collects and execute them.

    Buffer the last response, in case the new one is not ready (actors
    return promises and we leverage that).

    We could probably enhace this by spawning some actors of our own to
    collect metrics related with the host we're running in, http response
    times and other fluff information.
"""

import collections

import hollywood
import hollywood.actor


class Registry(object):
    """
        Spawn an actor for each subclass of poller.Base.

        Store that ActorRef so we can .ask() it for new
        data obtained from polling.
    """

    pollers = collections.OrderedDict()
    futures = []
    last_response = collections.OrderedDict()

    @classmethod
    def register(cls, actor, params):
        poller = hollywood.System.spawn(actor)
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
        for idx, actor in enumerate(cls.pollers.keys()):
            if not cls.futures[idx].ready():
                continue
            cls.last_response[idx] = cls.futures[idx].get()
            cls.futures[idx] = actor.ask(cls.pollers[actor])
        return '\n'.join(cls.last_response.values())
