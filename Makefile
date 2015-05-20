.PHONY: setup setup-dev

UNAME_S = $(shell uname -s)

setup:
ifeq ($(UNAME), Linux)
	pip install -r requirements/linux.txt
else
	pip install -r requirements/base.txt
endif

setup-dev: setup
	pip install -r requirements/dev.txt
