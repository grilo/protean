#!/usr/bin/env python

"""
    The most basic http server possible.

    It's only job is to get whatever the metrics poller has collected.

    Serves any kind of request, not exclusively /metrics.
"""

import logging
import time

import hollywood
import hollywood.net.http

import protean.poller


class MetricsResponseHandler(hollywood.actor.Threaded):

    def receive(self, request):
        response = hollywood.net.http.Response()
        response.content_type = 'text/plain'
        response.content = protean.poller.Registry.get()
        request.send(response)
        return response


def serve_forever(address='0.0.0.0', port=5000, certfile=None):
    handler = hollywood.System.spawn(MetricsResponseHandler)
    http_server = hollywood.System.spawn(hollywood.net.http.Server, handler)
    http_server.tell(address=address, port=port, certfile=certfile)

    while hollywood.System.alive():
        logging.info("Actors alive: %i", hollywood.System.alive())
        time.sleep(5)
