-- Export one row per (sample, composition) for the matchable DB subset:
-- H2SO4(aq) acid CP overpotential rows whose process concentration = 1 (= "1.0 M sulfuric acid").
-- comp = the raw composition json (nonzero cation fractions handled downstream).
copy (
  select distinct f.sample_id::text, f.sample_label, f.comp::text as comp
  from r0survey.acid_cp_fom f
  join r0survey.acid_sp a on a.sample_id=f.sample_id and a.technique=f.technique
  join public_release.process pr on pr.id=a.proc_id
  join public_release.process_detail pd on pd.id=pr.process_detail_id
  where f.eta_v_ave is not null
    and f.electrolyte='H2SO4(aq)'
    and jsonb_typeof(f.comp)='object'
    and (pd.parameters::jsonb->>'concentration') = '1'
) to stdout with (format csv, header true);
