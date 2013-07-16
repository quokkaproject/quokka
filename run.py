import sys
if len(sys.argv) > 1 and sys.argv[1] == "-r":
    reloader = True
else:
    reloader = False

from quokka import create_app
app = create_app()
app.run(use_reloader=reloader)
