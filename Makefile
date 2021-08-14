python = python3
# empty targets for recipes that don't produce actual targets
targets = .fake_targets
build = $(targets)/build
build-dev = $(targets)/build-dev
test = $(targets)/test
black = $(targets)/black

# python stuff
venv = .venv
bin = $(venv)/bin
srcdir = src
srcfiles = $(shell find $(srcdir) -name '*.py')
testdir = tests
testfiles = $(shell find $(testdir) -name '*.py')
codedirs = $(srcdir) $(testdir)
codefiles = $(srcfiles) $(testfiles)
mainprg = $(srcdir)/main.py

# order-only-prereqs
predirs = $(venv) $(targets)

###############################################################################

all: build

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
	touch $(build)
build-dev: $(build-dev)

$(test): $(srcfiles) $(testfiles) $(build-dev) | $(predirs)
	$(bin)/py.test $(testdir) -s
	touch $(test)
test: $(test)

$(black): $(codefiles) $(build-dev) | $(predirs)
	$(bin)/black $(codedirs)
	touch $(black)
black: $(black)

check: test black

$(targets):
	mkdir -p $(targets)

$(venv):
	$(python) -m venv $(venv)
	$(bin)/pip install pip-tools

clean:
	rm -r $(venv)
	rm -r $(targets)

shell:
	$(bin)/ipython

# PHONY means that these targets are to be run irrespective of a file called
# "clean"existing
.PHONY: clean run shell
