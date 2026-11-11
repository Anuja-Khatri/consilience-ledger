# For teams running autonomous labs

This page is for people who run automated or high-throughput labs. It explains, in plain words, what this repository does and why it might matter to you.

One rule governs everything here: every number comes with its sample size, and tests fail the build if a number drifts from its registered value. I built this in an AI-assisted sprint, reviewing and approving each decision, and the mistakes I made along the way are listed in a public corrections file. I assume your team has already solved some of the problems below. What I offer is an independent implementation you can check yourself in an afternoon.

The examples use public data: a high-throughput OER electrochemistry release (Caltech HTE, CC BY 4.0), a published nine-lab comparison study, and a published autonomous-lab benchmark. The chemistry is the test case. The machinery does not depend on it.

## 1. Two runs disagree. Is that real, or is it noise?

Run the same material twice and the numbers differ. By how much before it means something? Most pipelines guess. Guess too tight and you chase ghosts. Guess too loose and you miss real contradictions.

I measured it instead. Nine labs measured the same material. The central range across them is 90.7 mV (n=9). The comparison engine treats that measured spread as the floor. Fork counts are only ever reported with the threshold used: 0 to 4 forks at s = 15 mV (full sweep: 4, 15, 20, 23 forks at thresholds of 15, 10, 7.5 and 5 mV; n=36 pairs; 9 of 11 labs mappable).

What this gives you: when the system flags a disagreement, it has already cleared what normal lab-to-lab variation looks like. People investigate signal, not noise.

## 2. Results get compared that should never be compared

A number measured on glass gets plotted next to a number measured on silicon. A 15-second hold gets compared with a 10-minute hold. The plot looks fine, because numbers always look fine.

Here, every claim becomes a card that carries its conditions: material, value, substrate, hold time, electrolyte, and so on. A judge compares two cards. The judge is plain code. No AI inside it, no text input. Same cards in, same verdict out, every time, with a hash you can re-run. If the conditions do not match, it refuses to compare, and it names the condition that failed.

A real case from this repo: I compared two datasets. 7,115 pairs, 1,881 samples, 1,041 matched pairs across 58 compositions, 297 samples at the closest condition. The judge refused, because three recorded conditions fail independently: hold time, substrate, deposition method. And on a known pair of palladium papers that agree, it refused to invent a disagreement. The human review of those two cards, including the mistakes it caught, is public in the closure records.

What this gives you: cross-campaign comparisons become safe by default. The system says "not comparable, and here is why" instead of quietly averaging apples and oranges.

## 3. Bad records slip into every result store

Big result stores collect errors: transcription slips, impossible values, measurements that went past what the instrument was set to allow. This is normal. It happens in every lab and every database, ours included. Models train on those records. Decisions inherit them.

I ran the check on the public release this work builds on. A dataset of this size and age is expected to carry some slips; finding them is what the check is for, and it is no criticism of the people who made the data. I ingested 140,708 claim cards from that release (n=140,708) and sorted every comparison into six buckets, always reported together: not comparable 74,569; within floor 80,144; replicate inconsistency 0; fork 0; suspect transcription 16,613 (test half, under correction C-003); catalog untestable 6,231. A compliance pass found 5,131 of 70,152 records that went past their own recorded instrument limit by more than 0.5 V, plus 920 records with impossible values (overpotential at or below zero). The limit field itself was present in all 70,152. And on clean null data the pipeline invents nothing: false positive rate 0.000 (n=1,228, q=0.05).

What this gives you: run at ingest time, the same check catches bad records before they spread into models and decisions. A data team gets a typed defect list instead of a vague worry.

## 4. An agent wrote a plan. Is it safe to run?

Agent loops write experiment plans faster than people can review them. Manual review becomes the bottleneck, or it gets skipped.

I built a gate that checks each typed plan against typed safety rules in about 20 ms. Its record: 13,627 safe plans, zero wrongly blocked, zero passed to a human as unsure. 990 attack plans, zero through the typed gate. An LLM attacker scored 0 of 12 in a preregistered run, then 0 of 48 and 0 of 48 (exact confidence interval 0.00 to 0.074 per mode). A stronger attacking model reached 0.08 (n=36). The plan checker matched its spec on 12,000 of 12,000 plans. Replays were identical 458 of 458 times. One limit, stated rather than hidden: wording outside the typed vocabulary slips past the typed layer in 20.6% of cases (n=34).

The safety rules live in a format where each rule carries a grade and a source, compiled into machine checks with no text input. It ships with a six-rule demonstration seed, reviewed and signed by the owner, under a policy that keeps dangerous content permanently out, enforced by an automatic scan. Filling the format with your real safety content is your experts' work. The container, the compiler and the gate are done.

What this gives you: safety review that scales with the loop. Humans set the rules once. The gate enforces them on every plan, with an audit trail.

## 5. Which disagreement is worth your next experiment?

The most valuable thing a claims layer can produce is a short list: the contradictions in your results, ranked, each one resolvable by an experiment your platform can run.

Published papers cannot feed this. In my census, about 3 result sentences in 100 state the correction method, and a single material needs roughly 600 condition-complete claims where public sources give about 20.

So here is what I can prove, honestly. The hunting machinery exists and its accuracy is measured. When I planted disagreements, it found all of them: recovery 1.00 and 1.00 (n=33). On null data it invented none: false positives 0.000 (n=1,228, q=0.05). On public data the hunt ran and came back empty, and I publish that as a fact about public data. A separate cross-field matcher test also came back empty: 0 of 60 candidate pairs.

Your internal records are different. They carry exactly what papers drop: the conditions, as data. Pointed at a LIMS, an ELN or a platform's run store, the same engine surfaces inconsistent replicates and ranks contradictions. The planted-disagreement numbers are the evidence it works the moment the data exists. A full detect-and-write-back loop runs end to end on synthetic data (labelled synthetic, n=1 cycle); it is designed for live streams and has not yet run on one.

## 6. The pipeline was built with AI. Why trust it?

Fair question. My answer: do not trust it. Check it.

Every public number is registered with its sample size, and a test fails the build if it drifts. The repository rebuilds byte-identically from source. Pre-registrations were written before data was read. A corrections file lists every error found so far, including the assistant's own arithmetic error, each fixed in a visible commit. A human gate sits over extraction, and it earns its keep: on the two closure cards it caught a missing stated condition and an invented number, both corrected on the record, with the before and after preserved.

Where the AI sits, and where it does not: a language model reads sentences into cards. That step is the measured weak link. A prompt-injection probe steers extraction in 0.30 of cases overall and 0.91 in the worst class. That is exactly why the judge that issues verdicts has no text input at all, and why a human reviews cards. Judge agreement with hand verdicts: 1.0 (n=213), 1.0 (n=311), 0.9842 (n=316). One piece is a design only: a trace audit that would check each agent decision against the evidence available at that step. It needs private traces by definition, so it is not built.

What this gives you: trust that does not depend on taking my word. Every number has a receipt. Every mistake has a commit. Every unproven part says so.

## What I do not claim

I found no contradictions in public data; the buckets above say so. The write-back loop has run only on synthetic data. The typed safety layer has a stated blind spot. The trace audit is a design. Everything unproven here is labelled, and everything labelled proven can be rerun by you.

## Check it in an afternoon

Clone the repo. Run the tests and `make reproduce`. Read the numbers lock, the corrections file, and the closure records with both verdict hashes. Then judge the one claim this page makes: the same machinery, pointed at data that records its conditions, becomes the claims layer an autonomous lab needs.

Found a problem? Open an issue. Maintained by Anuja Khatri.
