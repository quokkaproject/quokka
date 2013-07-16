
import os
from flask.ext.script import Command, Option


class Test(Command):
    "Run tests."

    start_discovery_dir = "quokka/tests"

    def get_options(self):
        return [
            Option(
                '--start_discover', '-s', dest='start_discovery',
                help='Pattern to search for features',
                default=self.start_discovery_dir),
        ]

    def run(self, start_discovery):
        import unittest

        if os.path.exists(start_discovery):
            argv = ["quokka", "discover"]
            argv += ["-s", start_discovery]

            unittest.main(argv=argv)
        else:
            print("Directory '%s' was not found in project root." % start_discovery)
