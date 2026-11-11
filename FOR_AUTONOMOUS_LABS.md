# For teams running autonomous labs

If your team operates a self-driving or high-throughput experimentation platform, this page is the fastest way to understand what this repository is for. Everything claimed here is reproducible from this repo: every number carries its sample size, is registered in a numbers lock, and is enforced by tests that fail the build if it drifts. The pipeline was built in an AI-assisted sprint with a human owner reviewing and approving each decision; the commit history, the corrections file and the review trail are public on purpose. We assume teams running these platforms have solved many of these problems internally. What this repo offers is an independent, deterministic, receipts-first implementation that can be checked in an afternoon.

The worked examples use published materials: a public high-throughput OER electrochemistry release (Caltech HTE, CC BY 4.0), a published inter-laboratory benchmarking study, and a published autonomous-lab benchmark paper. The same machinery is domain-portable; the chemistry is the testbed, not the limit.

## Six problems every claims pipeline hits, and what is built here for each

### 1. Two runs disagree. Is that chemistry, or noise?

The pain. The same composition, measured twice, differs by tens of millivolts. Without knowing how far honest measurements naturally sit apart, every threshold for "real disagreement" is a guess, and guessed thresholds manufacture contradictions or bury them.

What is built. We measured the floor instead of assuming one. Across nine labs measuring the same material, the inter-lab central range is 90.7 mV (n=9). Fork counts are then reported only against a stated sensitivity: 0 to 4 forks at s = 15 mV (full sweep: 4, 15, 20, 23 forks at thresholds 15, 10, 7.5, 5 mV; n=36 pairs; 9 of 11 labs mappable). The comparison engine is calibrated to the measured floor.

What this improves. Replicate triage stops being a judgment call. A disagreement is flagged only when it clears what honest variation actually looks like, so people investigate real signal instead of noise.

### 2. Results get compared that were never comparable

The pain. Overpotentials from different substrates, hold times, deposition methods or correction protocols end up in the same plot or the same decision. The comparison looks numeric, so it looks valid.

What is built. Every claim is typed into a card that carries its conditions, and a deterministic judge (plain code, no model call, no text channel, same verdict every time, hash-reproducible) refuses any pair whose conditions do not match, with the reason typed into the refusal. Case study in this repo: a 7,115-pair comparison across two datasets (1,881 samples; 1,041 matched pairs across 58 compositions; 297 samples at the closest condition) was correctly refused because three recorded conditions fail independently: hold time, substrate, deposition method. On a known-answer pair of palladium papers that agree where they touch, the judge refused to manufacture a fork; the owner's review of those two cards, including the corrections it produced, is public in the closure records.

What this improves. Cross-campaign and cross-instrument comparisons become safe by construction. The system says "not comparable, and here is why" instead of quietly averaging apples and oranges.

### 3. The database everyone trusts carries silent defects

The pain. Large result stores accumulate transcription slips, nonphysical values and records that exceeded their own instrument limits. Downstream models train on them and downstream decisions inherit them.

What is built. On a 140,708-card ingest of the public release (n=140,708), every comparison is sorted into six classes, always reported together: not comparable 74,569; within floor 80,144; replicate inconsistency 0; fork 0; suspect transcription 16,613 (test half, under correction C-003); catalog untestable 6,231. The compliance pass found 5,131 of 70,152 records exceeding their own recorded instrument limit by more than 0.5 V, and 920 more with nonphysical values (overpotential at or below zero). The limit field was present in 70,152 of 70,152 records. On null data the pipeline invents nothing: false positive rate 0.000 (n=1,228, q=0.05).

What this improves. Run at ingest time, this catches defects before they propagate into models, dashboards or the next campaign's priors, and it gives data stewards a typed defect list instead of a vague cleanliness worry.

### 4. An agent is about to run a plan. Is it safe, and is it in spec?

The pain. Agentic loops generate experiment plans faster than humans can review them. Manual safety review becomes the bottleneck or gets skipped; a single out-of-spec plan can damage an instrument or worse.

What is built. A pre-run gate checks each typed plan against typed safety rules in about 20 ms. Record: zero false blocks on 13,627 benign plans with zero abstentions, and zero attacks through the typed gate on 990 adversarial plans. An LLM attacker scored 0 of 12 preregistered attempts, then 0 of 48 and 0 of 48 (exact CI 0.00 to 0.074 per mode); a stronger attacking model reached 0.08 (n=36). Plan checker exactness 1.0 (n=12,000); replay determinism 1.0 (n=458). Disclosed limit: phrasing outside the typed vocabulary evades the typed layer in 20.6% of cases (n=34); the layer's scope is stated, not hidden. The rule format ships with a grade ladder, per-rule sources, a compiler to machine checks with no text channel, and an owner-signed benign seed (safety-seed-v1) under a policy that keeps dual-use content permanently out of scope, enforced by a denylist scan.

What this improves. Safety review scales with the loop instead of throttling it. Humans set the rules once, with sources and grades; the gate enforces them on every plan, deterministically, with an audit trail. Filling the format with a real lab's EHS content is domain scientists' work; the container, compiler and gate are done.

### 5. Which disagreement deserves the next experiment?

The pain. The most valuable output of a claims layer is a ranked list of contradictions worth resolving: forks that an autonomous lab could turn directly into experiments. Published text cannot feed this. In our census, roughly 3 in 100 result sentences state the correction method, and a material needs on the order of 600 condition-complete claims where public sources yield about 20.

What is built, and what is proven. The hunting machinery exists and its accuracy is measured: on planted forks, recovery 1.00 and 1.00 (n=33); on null data, false positives 0.000 (n=1,228, q=0.05). On public data the hunt ran honestly and returned empty, and we publish that as a measurement of public data, not as a success. A separate cross-field structural matcher test returned a true null, 0 of 60 candidate pairs, reported with its denominator.

What this improves, given internal data. Lab records carry exactly what public text drops: conditions, as data. Pointed at an ELN, a LIMS or an autonomous platform's run store, the same engine surfaces replicate inconsistencies and ranks contradictions by how cheaply the platform could resolve them. The planted-fork numbers are the evidence this works the moment condition-complete data exists. A full detect-to-writeback loop is demonstrated end to end on synthetic data (labelled synthetic, n=1 cycle); it is designed to run on live streams and has not yet been run on one.

### 6. The pipeline was built with AI. Why should anyone trust it?

The pain. AI-assisted pipelines produce confident numbers with no chain of custody. For a lab whose output is scientific claims, an unauditable pipeline is a liability regardless of its accuracy.

What is built. The repo polices itself in public: preregistrations written before data is read; stop rules that have fired and held; a numbers lock registering every public number with its n, linted in CI; byte-stable reproduction from source; and a corrections file listing every error found so far, including the assistant's own arithmetic error, each fixed in a visible commit. A human review gate sits over extraction, and it works: on the closure cards it caught a wrongly omitted stated condition and an invented number, both corrected on the record with pre-review and post-review verdicts preserved. Engine validation: verdict agreement 1.0 (n=213), 1.0 (n=311), 0.9842 (n=316). Extraction is the measured weak link and is treated as such: a prompt-injection probe steers extraction in 0.30 of cases overall and 0.91 in the worst class, which is exactly why the judge has no text channel and why a human gate sits over extraction. A trace audit, checking each agent decision against the evidence recorded at that step, is designed but not built; it needs private traces by definition.

What this improves. Trust stops being a vibe. Every number has a receipt, every mistake has a commit, and the parts that are unproven say so in plain words.

## What we do not claim

No contradictions were discovered in public data; the buckets say so. The write-back loop has run only on synthetic data. The typed safety layer has a stated blind spot. The trace audit is a design. Anything in this repo that is not proven is labelled, and anything labelled proven can be rerun.

## Check this in an afternoon

Clone the repo. Run the test suite and `make reproduce`; the build is byte-stable. Read NUMBERS_LOCK, the corrections file, and the closure records with both verdict hashes. Then judge the claim this page actually makes: that the same machinery, held to the same standard, pointed at data that records its conditions, becomes the claims layer an autonomous lab needs.

Questions, objections and broken things: open an issue. Maintained by Anuja Khatri.
