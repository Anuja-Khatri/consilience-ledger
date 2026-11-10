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

ledger:
	$(PY) -m labext.ledger

# Regenerate the deterministic artifacts and verify the suite. The ledger hash must
# stay byte-identical from the approved cards + rules.lock + code version (spec IV.5).
reproduce: schemas lock ledger test
	@echo "reproduce OK: schemas + rules.lock + ledger regenerated, tests green"
