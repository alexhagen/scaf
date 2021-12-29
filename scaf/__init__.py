import argparse
import sys
import glob
import os
import pathlib
import logging
import json

HOME = os.path.expanduser("~")
SCAFDIR = os.path.join(HOME, '.scaf')
SCAFFILESDIR = os.path.join(SCAFDIR, 'files')
SNIPPETSFILE = os.path.join(SCAFDIR, 'snippets.json')


## Check for scaffolding directory, if it doesn't exist, create it
if not os.path.isdir(SCAFDIR):
    pathlib.Path(SCAFFILESDIR).mkdir(parents=True, exist_ok=True)
    with open(SNIPPETSFILE) as f:
        f.write('[]')
    
# Open the snippets and files directory
SNIPPETS = []
with open(SNIPPETSFILE) as f:
    SNIPPETS = json.load(f)

class Scaf(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Scaffolding for simple ' +
                                         'dev tasks',
                                         usage='scaf <command> [<args>]')
        parser.add_argument('command', help='subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('unrecognized command')
            parser.print_help()
            sys.exit(1)
        self.args = sys.argv[2:]
        getattr(self, args.command)()

    def p(self):
        self.print()

    def print(self):
        identifier = self.args[0]
        for snippet in SNIPPETS:
            snippet_name = list(snippet.keys())[0]
            snippet_keywords = snippet[snippet_name]['keywords']
            snippet_text = snippet[snippet_name]['text']
            if identifier == snippet_name:
                print(snippet_text)
                return
            elif ',' not in identifier:
                if identifier in snippet_keywords:
                    print(f'NAME: {snippet_name}')
                    print(snippet_text)
            elif ',' in identifier:
                identifiers = identifier.split(',')
                if all([_i in snippet_keywords for _i in identifiers]):
                    print(f'NAME: {snippet_name}')
                    print(snippet_text)
        return

    def l(self):
        self.list()

    def list(self):
        for snippet in SNIPPETS:
            snippet_name = list(snippet.keys())[0]
            snippet_keywords = snippet[snippet_name]['keywords']
            print(f'{snippet_name:30s}: {str(snippet_keywords):48s}')
        return

    def lf(self):
        self.list_files()

    def list_files(self):
        for file in glob.glob(os.path.join(SCAFFILESDIR, '*')):
            print(os.path.basename(file))
        return

    def pf(self):
        self.print_file()

    def print_file(self):
        file = self.args[0]
        path = os.path.join(SCAFFILESDIR, file)
        if os.path.isfile(path):
            with open(path) as f:
                string = f.read()
            print(string)
        else:
            raise Exception("No such file in templates")

    #def doc(self):
    #    """Add in documentation."""
    #    parser = argparse.ArgumentParser(description="Add documentation folder "
    #                                     + "and perform sphinx-quickstart")
    #    parser.add_argument('author', default='Alex Hagen', nargs='?')
    #    parser.add_argument('version', default='0.0.1', nargs='?')
    #    args = parser.parse_args(sys.argv[2:])
    #    self.version = args.version
    #    self.author = args.author
    #    print("generating documentation folder")
    #    # make directory doc
    #    (Path(self.cwd) / Path('doc')).mkdir(parents=True, exist_ok=True)
    #    # add line to top level Makefile
    #    self._prepend_pyfiles()
    #    with open(self.makefilename, 'a') as f:
    #        f.write('doc: doc/source/conf.py doc/Makefile doc/source/*.rst ' +
    #                '$(PYFILES)\n')
    #        f.write('\tcd doc\n')
    #        f.write('\tmake markdown\n')
    #        f.write('\n')
    #    # pipe sphinx-quickstart commands and returns through the command line
    #    command = f'sphinx-quickstart -p {self.project_name} ' + \
    #        f'-a "{self.author}" -r {self.version} ' + \
    #        f'-v {self.version} -l en --sep --no-batchfile --ext-autodoc ' + \
    #        '--ext-coverage --ext-mathjax --ext-intersphinx'
    #    print(command)
    #    os.chdir('doc')
    #    os.system(command)
    #    os.chdir('../')
    #    return self
#
    #def test(self):
    #    """Add in testing."""
    #    parser = argparse.ArgumentParser(description='Add testing folder ' +
    #                                     'and set up testing makefile target')
    #    print("generating test folder")
    #    (Path(self.cwd) / Path('test')).mkdir(parents=True, exist_ok=True)
    #    # add line to top of Makefile
    #    self._prepend_tests()
    #    # add line to top level Makefile
    #    with open(self.makefilename, 'a') as f:
    #        f.write('test: $(PYFILES) $(TESTS)\n')
    #        f.write('\tpytest --ignore=sandbox/ --cov=./ --cov-report=html ' +
    #                '--cov-config=.coveragerc ' +
    #                '| tee doc/source/_static/doc_test.txt\n')
    #        f.write('\n')
    #    return self
#
    #def _prepend_pyfiles(self):
    #    if os.path.isfile(self.makefilename):
    #        with open(self.makefilename, 'r') as original:
    #            data = original.read()
    #    else:
    #        data = ''
    #    if 'PYFILES :=' not in data:
    #        with open(self.makefilename, 'w') as modified:
    #            modified.write(f'PYFILES := $(wildcard {self.project_name}' +
    #                           '/*.py)\n' + data)
#
    #def _prepend_tests(self):
    #    self._prepend_pyfiles()
    #    with open(self.makefilename, 'r') as original:
    #        data = original.read()
    #    with open(self.makefilename, 'w') as modified:
    #        modified.write('TESTS := $(wildcard test/test_*.py)\n\n' + data)
#
    #def todo(self):
    #    """Add in todo listing."""
    #    parser = argparse.ArgumentParser(description='Add a todo target to ' +
    #                                   'the Makefile')
    #    self._prepend_pyfiles()
    #    with open(self.makefilename, 'a') as f:
    #        f.write('todo: $(PYFILES)\n')
    #        f.write('\tleasot $(PYFILES) --filetype=.py | tee -a todos.md\n')
    #    return self
#
    #def article(self):
    #    """Start a latex article."""
    #    parser = argparse.ArgumentParser(description='Make a folder with ' +
    #                                     'boilerplate for a latex article')
    #    parser.add_argument('name', default='article')
    #    parser.add_argument('path', default='doc', nargs='?')
    #    parser.add_argument('template', default='article', nargs='?')
    #    args = parser.parse_args(sys.argv[2:])
    #    article_name = args.name
    #    article_path = Path(args.path) / Path(article_name)
    #    Path(article_path).mkdir(parents=True, exist_ok=True)
    #    # TODO[ahagen]: read templates from ~/.scaf/templates/
    #    # TODO[ahagen]: if the templates dont exist, save from github
    #    material = {'Makefile': "content",
    #                'main.tex': "content",
    #                'ref.bib': "content"}
    #    for filename, content in material.items():
    #        with open(Path(article_path) / Path(filename), 'w') as f:
    #            f.write(content)
    #    return self

#def _make_parser():
#    parser = argparse.ArgumentParser(description='Scaffolding for simple ' +
#                                     'dev tasks',
#                                     usage='scaf <command> [<args>]')
#    return parser

def _run_cli(): # pragma: no cover
    #args = _make_parser().parse_args()
    #logging.basicConfig(format='%(levelname)s:%(message)s',
    #                    level=args.logging_level)
    scaf = Scaf()


if __name__ == "__main__":
    _run_cli()
