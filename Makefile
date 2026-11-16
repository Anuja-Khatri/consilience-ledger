PY=.venv/bin/python

# Every target is phony. "ledger" in particular shares its name with the ledger/
# directory: without this line make printed "'ledger' is up to date" and silently
# skipped the ledger rebuild inside `make reproduce`.
.PHONY: setup test schemas lock ledger verdicts reproduce check-unchanged

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

# Writeback needs Lila's data at runtime (env LILA_OER_DATA_DIR or the upstream checkout);
# it is never committed (CC-28). Without the data it says so and leaves the committed
# verdicts unchanged (the ledger rebuild no longer empties them either).
verdicts:
	$(PY) -m labext.writeback

# Fail loudly if regeneration changed any committed artifact.
check-unchanged:
	@git diff --exit-code --stat -- ledger reports schema rules/rules.lock \
	  || { echo "reproduce FAILED: regenerated artifacts differ from the committed ones (diff above)"; exit 1; }

# Regenerate the deterministic artifacts, verify they are byte-identical to the committed
# ones, and run the suite. The ledger hash must stay byte-identical from the approved
# cards + rules.lock + code version (spec IV.5).
reproduce: schemas lock ledger verdicts check-unchanged test
	@echo "reproduce OK: schemas + rules.lock + ledger rebuilt byte-identical, verdicts checked, tests green"
