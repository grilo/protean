#!/usr/bin/env python

import logging
import time
import random

import hollywood.actor

import poller
import meter


def metric_decorator(metric):
    """Return a specially crafted actor to be used as a collector.

    We're just doing this trickery for API-friendliness:

        from protean.decorators import *

        @counter('a_special_counter', 'a description')
        def something(*args):
            return "10"
    """


    def real_decorator(function):

        class MetricActor(hollywood.actor.Threaded):
            def receive(self, function):
                result = function()
                if not isinstance(result, tuple):
                    result = result, {}
                return self.metric.measure(result[0], **result[1]).to_string()

        actor = MetricActor
        actor.metric = metric
        actor.address = [__name__.replace('.', '/') + '/' + function.__name__]
        poller.Registry.register(actor, function)
    return real_decorator


def gauge(name, description=None):
    return metric_decorator(meter.Gauge(name, description))

def counter(name, description=None):
    return metric_decorator(meter.Counter(name, description))

def summary(name, buckets, description=None):
    return metric_decorator(meter.Summary(name, buckets, description))

def histogram(name, buckets, description=None):
    return metric_decorator(meter.Histogram(name, buckets, description))
