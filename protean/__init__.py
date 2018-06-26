#!/usr/bin/env python

import hollywood
import http

def start():
    hollywood.System.init()
    http.serve_forever()
