-- Check 1b: distribution of acid CP overpotential rows (the MPS adapter's selection)
-- Selection mirrors engine/adapters/mps.py: eta_v_ave not null, electrolyte in the two acids,
-- comp is a json object. Counts by electrolyte identity x pH x technique.
select f.electrolyte, f.ph_raw, f.technique, count(*) as n_rows,
       count(distinct f.sample_id) as n_samples
from r0survey.acid_cp_fom f
where f.eta_v_ave is not null
  and f.electrolyte in ('H2SO4(aq)','KH2PO4/K2HPO4(aq)')
  and jsonb_typeof(f.comp) = 'object'
group by f.electrolyte, f.ph_raw, f.technique
order by n_rows desc;
