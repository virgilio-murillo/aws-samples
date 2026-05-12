VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python
FIND_NB := find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -not -path "*/investigation/*" -not -path "*/kiro-*"

.PHONY: lint validate strip-check test-mac

$(VENV):
	python3 -m venv $(VENV) && $(PIP) install -q -r requirements-ci.txt

lint: $(VENV)
	$(VENV)/bin/ruff check .

validate: $(VENV)
	$(PY) scripts/validate_notebooks.py

strip-check: $(VENV)
	$(FIND_NB) -exec $(VENV)/bin/nbstripout --verify {} +

test-mac: lint validate strip-check
	@echo "All checks passed."
