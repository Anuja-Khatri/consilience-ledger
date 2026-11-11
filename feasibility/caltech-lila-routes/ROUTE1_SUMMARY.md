# Route 1 summary: can a published screening set be condition-matched to a public database?

Route 1 matches Lila's published acid-OER screening rows (arXiv:2609.30133, their public repo)
against the Materials Provenance Store (MPS, CaltechDATA hjfx4-a8r81, CC BY 4.0) by composition,
in identical 1.0 M sulfuric acid, and then asks whether any matched pair states enough recorded
conditions to be compared. The full receipts are in route1_receipts/ in this folder; the numbers
below are reproduced from those committed tables.

## The matched set
- 1,125 Lila rows with valid composition, matched against 69,273 MPS samples in 1.0 M sulfuric
  acid.
- 7,115 matched row-sample pairs.
- 1,881 distinct MPS samples matched.

## The CP4 at +100 microamps subset
- 297 MPS samples.
- 1,041 of the 7,115 pairs involve at least one such sample.
- Distinct composition-match groups involved: 58 on the Lila side, 32 on the MPS side, over 5
  element systems.

## The recorded conditions on the matched samples
- Measurement holds are 10 or 15 seconds; 2,348 of 2,472 rows are at 15 seconds.
- Substrates are all glass: Glass FTO Tec 15 on 928 samples, Glass FTO Tec 7 on 900, and
  molybdenum-on-glass on 53.
- Fabrication is inkjet on 1,881 of 1,881 samples.
- Anneal maximum temperature: 350 C on 1,603 samples, 450 C on 171, 300 C on 53, 605 C on 27,
  and 600 C on 27.

By contrast, Lila's own screening hold is published as the overpotential at 10 mA per cm2 after
10 minutes (quoted from arXiv:2609.30133 section 1a). The matched database measurements are
10-to-15-second holds, a different measurement from the published 10-minute screening point.

## The verdict
Every pairing is refused on recorded conditions: the two sides never state the same conditions
closely enough to be compared. That refusal is the comparison instrument doing its job, not a
failure to find a match.

## Check 3 (McCrory tables)
Of 57 approved claim cards, 0 are condition-complete against the McCrory benchmark tables. The
McCrory Supporting Information carries restrictive rights, so its texts are not included in this
repo; only the derived count is reported.
