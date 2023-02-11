.PHONY: run clean

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

#run: $(VENV)/bin/activate

install: requirements.txt
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
