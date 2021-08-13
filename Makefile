# empty targets for recipes that don't produce actual targets
targets = .fake_targets
build = $(targets)/build
build-dev = $(targets)/build-dev
test = $(targets)/test
mypy = $(targets)/mypy
black = $(targets)/black

# python stuff
venv = .venv
bin = $(venv)/bin
codedir = inhabit
codefiles = $(shell find $(codedir) -name '*.py')
testdir = tests
testfiles = $(shell find $(testdir) -name '*.py')
srcdirs = $(codedir) $(testdir)
srcfiles = $(codefiles) $(testfiles)
mainprg = $(codedir)/main.py

# order-only-prereqs
predirs = $(venv) $(targets)

###############################################################################

all:
	@echo Please give a command

requirements.txt: requirements.in | $(predirs)
	$(bin)/pip-compile requirements.in

dev-requirements.txt: dev-requirements.in | $(predirs)
	$(bin)/pip-compile dev-requirements.in

# A rule will run if the target does not exist, a pre-req does not exist, or a
# pre-req is newer than the target. Since the python build process doesn't
# produce an actual output file we will `touch .fake_targets/build` at the end
# to replicate the behaviour of an actual output file.
$(build): requirements.txt | $(predirs)
	$(bin)/pip-sync requirements.txt
	touch $(build)
# Aliasing `.build` to `build` so devs can type `make build`
build: $(build)
# This same pattern is used for build-dev, test, mypy, black etc


$(build-dev): requirements.txt dev-requirements.txt | $(predirs)
	$(bin)/pip-sync requirements.txt dev-requirements.txt
	touch $(build-dev)
build-dev: $(build-dev)

$(test): $(codefiles) $(testfiles) $(build-dev) | $(predirs)
	$(bin)/py.test $(testdir) -s
	touch $(test)
test: $(test)

$(black): $(srcfiles) $(build-dev) | $(predirs)
	$(bin)/black $(srcdirs)
	touch $(black)
black: $(black)

$(mypy): $(srcfiles) $(build-dev) | $(predirs)
	$(bin)/mypy $(srcdirs)
	touch $(mypy)
mypy: $(mypy)

check: test mypy black

$(targets):
	mkdir -p $(targets)

$(venv):
	python -m venv $(venv)
	$(bin)/pip install pip-tools

clean:
	rm -r $(venv)
	rm -r $(targets)

run:
	.venv/bin/python main.py

shell:
	.venv/bin/ipython

# PHONY means that these targets are to be run irrespective of a file called
# "clean"existing
.PHONY: clean run shell