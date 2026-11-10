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

# Writeback needs Lila's data at runtime (env LILA_OER_DATA or the upstream checkout);
# it is never committed (CC-28). Without the data it writes empty verdicts and continues.
verdicts:
	$(PY) -m labext.writeback

# Regenerate the deterministic artifacts and verify the suite. The ledger hash must
# stay byte-identical from the approved cards + rules.lock + code version (spec IV.5).
reproduce: schemas lock ledger verdicts test
	@echo "reproduce OK: schemas + rules.lock + ledger + verdicts regenerated, tests green"
