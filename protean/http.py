import logging
import time

import hollywood.http

import poller


class MetricsResponseHandler(hollywood.actor.Threaded):

    address = [
        'MetricsResponseHandler',
    ]

    def receive(self, request):
        response = hollywood.http.Response()
        response.content_type = 'text/plain'
        response.content = poller.Registry.get()
        request.send(response)
        return response


def serve_forever(port=5000):
    hollywood.System.init()
    http_server = hollywood.System.new('hollywood/http/Server')
    http_server.tell(port=port, response_handler='MetricsResponseHandler')

    while hollywood.System.status()['processes'] > 0:
        status = hollywood.System.status()
        logging.info("Registered: %i, Alive: %i", status['addresses'], status['processes'])
        time.sleep(2)
