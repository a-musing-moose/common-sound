.PHONY: setup

UNAME_S = $(shell uname -s)

setup:
ifeq ($(UNAME), Linux)
	pip install -r requirements/linux.txt
else
	pip install -r requirements/linux.txt
endif
