import argparse
from pathlib import Path
import sys
import os


class scaf(object):
    def __init__(self):
        # find some context variables
        self.cwd = os.getcwd()
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
        """Add in documentation."""
        parser = argparse.ArgumentParser(description="Add documentation folder "
                                         + "and perform sphinx-quickstart")
        parser.add_argument('author', default='Alex Hagen', nargs='?')
        parser.add_argument('version', default='0.0.1', nargs='?')
        args = parser.parse_args(sys.argv[2:])
        self.version = args.version
        self.author = args.author
        self.project_name = os.path.basename(os.path.normpath(self.cwd))
        print("generating documentation folder")
        # make directory doc
        (Path(self.cwd) / Path('doc')).mkdir(parents=True, exist_ok=True)
        # add line to top level Makefile
        with open(Path(self.cwd) / Path('Makefile'), 'a') as f:
            f.write('doc: doc/source/conf.py doc/Makefile doc/source/*.rst $(PYFILES)\n')
            f.write('\tcd doc\n')
            f.write('\tmake markdown\n')
            f.write('\n')
        # pipe sphinx-quickstart commands and returns through the command line
        command = f'sphinx-quickstart -p {self.project_name} -a "{self.author}" -r {self.version} -v {self.version} ' + \
            f'-l en --sep --no-batchfile --ext-autodoc --ext-coverage --ext-mathjax --ext-intersphinx'
        print(command)
        os.chdir('doc')
        os.system(command)
        os.chdir('../')

if __name__ == "__main__":
    scaf()