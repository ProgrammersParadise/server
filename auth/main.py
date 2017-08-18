#!/usr/bin/env python3

from env import Env
import webserver

if __name__ == '__main__':
    with Env() as env:
        webserver.serve(env)
