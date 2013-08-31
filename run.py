#!/usr/bin/env python
import argparse

from quokka import create_app

parser = argparse.ArgumentParser(description="Run Quokka App")
parser.add_argument('-p', '--port', help='App Port')
parser.add_argument('--host', help='App Host')
parser.add_argument('-r', action='store_true', help='Turn reloader on')
args = parser.parse_args()

host = args.host or 'localhost'
port = int(args.port) or 5000
reloader = args.r or False

print "####### HOSTS"
print host, port, reloader

app = create_app()
app.run(use_reloader=reloader, host=host, port=port)
