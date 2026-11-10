PY=.venv/bin/python

.PHONY: setup test schemas lock reproduce

setup:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

test:
	$(PY) -m pytest tests -q

schemas:
	$(PY) -m labext.gen_schemas

lock:
	$(PY) -m labext.lock

# Regenerate the deterministic artifacts and verify the suite. Grows to regenerate
# the full ledger in later phases; must stay byte-identical (spec IV.5).
reproduce: schemas lock test
	@echo "reproduce OK: schemas + rules.lock regenerated, tests green"
