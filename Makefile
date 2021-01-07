TESTS := $(wildcard test/test_*.py)

PYFILES := $(wildcard scaf/*.py)

todo: $(PYFILES)
	leasot $(PYFILES) --filetype=.py | tee -a todos.md

doc: doc/source/conf.py doc/Makefile doc/source/*.rst $(PYFILES)
	cd doc
	make markdown

test: $(PYFILES) $(TESTS)
	pytest --ignore=sandbox/ --cov=./ --cov-report=html --cov-config=.coveragerc | tee doc/doc_test.txt

