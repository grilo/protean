#!/usr/bin/env python

import logging
import argparse

import protean.http


def main(): # pragma: nocover
    desc = "Simple prometheus exporter."
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-a", "--address",
                        help="The IP address the exporter should bind to.",
                        default='0.0.0.0')
    parser.add_argument("-p", "--port",
                        help="The port the exporter should listen to.",
                        default=8000)
    parser.add_argument("-c", "--certfile",
                        help="The certificate (PEM). Optional, if you need https.")
    parser.add_argument("-v", "--verbose",
                        help="Increase output verbosity",
                        action="store_true")

    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s::%(levelname)s::%(module)s::%(message)s')
    logging.getLogger().setLevel('INFO')

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('Verbose mode activated.')

    protean.http.serve_forever(args.address, args.port, args.certfile)


if __name__ == '__main__': # pragma: nocover
    main()
