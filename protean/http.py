import logging
import time

import hollywood
import hollywood.net.http

import poller


class MetricsResponseHandler(hollywood.actor.Threaded):

    def receive(self, request):
        response = hollywood.net.http.Response()
        response.content_type = 'text/plain'
        response.content = poller.Registry.get()
        request.send(response)
        return response


def serve_forever(address='0.0.0.0', port=5000, certfile=None):
    handler = hollywood.System.new(MetricsResponseHandler)
    http_server = hollywood.System.new(hollywood.net.http.Server, handler)
    http_server.tell(address=address,
                     port=port,
                     certfile=certfile)

    while hollywood.System.alive():
        logging.info("Actors running: %i", hollywood.System.alive())
        time.sleep(2)
