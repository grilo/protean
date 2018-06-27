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


def serve_forever(address='0.0.0.0', port=5000, certfile=None):
    hollywood.System.init()
    http_server = hollywood.System.new('hollywood/http/Server')
    http_server.tell(address=address,
                     port=port,
                     certfile=certfile,
                     response_handler='MetricsResponseHandler')

    while hollywood.System.status()['processes'] > 0:
        status = hollywood.System.status()
        logging.info("Registered: %i, Alive: %i", status['addresses'], status['processes'])
        time.sleep(2)
