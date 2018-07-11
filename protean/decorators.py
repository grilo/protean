#!/usr/bin/env python

"""
    This module is pure syntatic sugar, there's no actual functionality.

    You decorate any function with the type of metric you want to collect,
    passing on to the decorator itself any relevant data regarding that
    specific metric.

    This dynamically generates an object (yay, python!) thus keeping state
    transparently.
"""

import hollywood.actor

import protean.poller
import protean.meter


def metric_decorator(metric):
    """Return a specially crafted actor to be used as a collector.

    We're just doing this trickery for API-friendliness:

        from protean.decorators import *

        @counter('a_special_counter', 'a description')
        def something(*args):
            return "10"

    We have to keep our own declaration of an actor since we change
    alot of its attributes ensuring its uniqueness. Instead of this
    fancy stuff, the user could instead create its own actor for
    each metric they want to collect but that's often too much
    overhead for such a simple task.

    Anyways, if you need very fancy stuff you probably shouldn't be
    using a random project found on the internet.
    """

    def real_decorator(function):

        class MetricActor(hollywood.actor.Threaded):
            def receive(self, function):
                result = function()
                if not isinstance(result, tuple):
                    result = result, {}
                return self.metric.measure(result[0], **result[1]).to_string()

        actor = MetricActor
        # Generate a unique name for this actor, otherwise the whole actor system
        # gets messed up when multiple actors with the same name get added. This
        # is likely masking UID problems.
        actor.__name__ = '/'.join([actor.__name__, function.__module__, function.__name__])
        actor.metric = metric
        protean.poller.Registry.register(actor, function)
    return real_decorator


def gauge(name, description=None):
    return metric_decorator(protean.meter.Gauge(name, description))

def counter(name, description=None):
    return metric_decorator(protean.meter.Counter(name, description))

def summary(name, buckets, description=None):
    return metric_decorator(protean.meter.Summary(name, buckets, description))

def histogram(name, buckets, description=None):
    return metric_decorator(protean.meter.Histogram(name, buckets, description))
