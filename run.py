#!/usr/bin/env python
import argparse
from quokka import create_app

parser = argparse.ArgumentParser(description="Run Quokka App")
parser.add_argument('-p', '--port', help='App Port')
parser.add_argument('-i', '--host', help='App Host')
parser.add_argument('-r', '--reloader', action='store_true',
                    help='Turn reloader on')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Turn debug on')
args = parser.parse_args()

app = create_app()
app.run(
    use_reloader=args.reloader or False,
    use_debugger=args.debug or False,
    host=args.host or '127.0.0.1',
    port=int(args.port) if args.port else 5000
)
