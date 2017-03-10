.PHONY: test install fmt upload ci

VIRTUALENV = $(shell which virtualenv)

ifeq ($(strip $(VIRTUALENV)),)
  VIRTUALENV = /usr/local/python/bin/virtualenv
endif


install: venv
	. venv/bin/activate; pip install --editable .

nopyc:
	find . -name '*.pyc' | xargs rm -f || true
	find . -name __pycache__ | xargs rm -rf || true

clean: nopyc
	rm -rf build python-boxconfig.egg-info venv

venv:
	$(VIRTUALENV) --python=python3 venv
