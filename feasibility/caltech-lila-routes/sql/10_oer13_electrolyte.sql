-- Determine the electrolyte of the oer13_cps simulator dataset (helao-async).
-- The dataset replays stored CP traces from plates 2750 and 3851 (the two plate keys in
-- oer13_cps.pzstd). This query reads the electrolyte those plates were actually measured in.
-- Result (CP3): NaOH(aq), concentration 0.35, solution_ph = 13, "0.1 M sodium hydroxide +
-- 0.25 M sodium sulfate" -> ALKALINE (OER13), pH 13, NOT acid. (The helao Electrolyte enum lists
-- OER13 separately from 1MH2SO4 and 1MNaOH.) An acid disagreement (Lila/MPS 1 M H2SO4, pH ~0)
-- cannot be run on a pH-13 simulator -- a ~13-unit pH gap.
select c.label as plate,
       pd.technique,
       pd.parameters::jsonb->>'electrolyte'          as electrolyte,
       pd.parameters::jsonb->>'concentration'        as concentration,
       pd.parameters::jsonb->>'solution_ph'          as solution_ph,
       pd.parameters::jsonb->>'solution_description' as solution_description,
       count(distinct cs.sample_id) as n_samples
from public_release.collection c
join public_release.collection__sample cs on cs.collection_id = c.id
join public_release.sample_process sp on sp.sample_id = cs.sample_id
join public_release.process pr on pr.id = sp.process_id
join public_release.process_detail pd on pd.id = pr.process_detail_id
where c.label in ('2750','3851') and pd.technique = 'CP3' and pd.parameters::jsonb ? 'electrolyte'
group by 1,2,3,4,5,6 order by plate, n_samples desc;
