#!/usr/bin/python

import argparse
from werkzeug.serving import run_simple
from quokka import create_app

application = app = create_app(ADMIN_REQUIRES_LOGIN=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Quokka App for WSGI")
    parser.add_argument('-p', '--port', help='App Port')
    parser.add_argument('-i', '--host', help='App Host')
    parser.add_argument('-r', '--reloader', action='store_true',
                        help='Turn reloader on')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Turn debug on')
    args = parser.parse_args()
    run_simple(
        args.host or '127.0.0.1',
        int(args.port) if args.port else 5000,
        application,
        use_reloader=args.reloader or False,
        use_debugger=args.debug or False,
    )
