-- Enriched per-sample export for the matchable subset (H2SO4(aq), process concentration=1):
-- sample composition + its anneal max_temperature + its plate (collection label) + plate data DOI.
copy (
  with base as (
    select distinct f.sample_id, f.sample_label, f.comp::text as comp
    from r0survey.acid_cp_fom f
    join r0survey.acid_sp a on a.sample_id=f.sample_id and a.technique=f.technique
    join public_release.process pr on pr.id=a.proc_id
    join public_release.process_detail pd on pd.id=pr.process_detail_id
    where f.eta_v_ave is not null and f.electrolyte='H2SO4(aq)'
      and jsonb_typeof(f.comp)='object' and (pd.parameters::jsonb->>'concentration')='1'
  ),
  ann as (
    select sp.sample_id, max((pd.parameters::jsonb->>'max_temperature')::float) as anneal_maxT
    from public_release.sample_process sp
    join public_release.process pr on pr.id=sp.process_id
    join public_release.process_detail pd on pd.id=pr.process_detail_id
    where pd.type='anneal'
    group by sp.sample_id
  ),
  col as (
    select cs.sample_id, string_agg(distinct c.label, ';') as plates, string_agg(distinct c.doi, ';') as dois
    from public_release.collection__sample cs
    join public_release.collection c on c.id=cs.collection_id
    group by cs.sample_id
  )
  select b.sample_id::text, b.sample_label, b.comp, an.anneal_maxT, co.plates, co.dois
  from base b
  left join ann an on an.sample_id=b.sample_id
  left join col co on co.sample_id=b.sample_id
) to stdout with (format csv, header true);
