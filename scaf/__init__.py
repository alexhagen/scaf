import argparse

class scaf(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Scaffolding for simple dev tasks',
                                         usage='scaf <command> [<args>]')
        parser.add_argument('command', help='subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('unrecognized command')
            parser.print_help()
            sys.exit(1)
        getattr(self, args.command)()

    def doc(self):
        parser = argparse.ArgumentParser(description="Add documentation folder "
                                         + "and perform sphinx-quickstart")
        args = parser.parse_args(sys.argv[2:])
        # make directory doc
        # add line to top level Makefile
        # pipe sphinx-quickstart commands and returns through the command line