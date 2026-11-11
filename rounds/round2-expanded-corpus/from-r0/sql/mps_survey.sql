-- R0 MPS survey (research only). Rebuilds the r0survey tables and the key numbers.
create schema if not exists r0survey;

-- acidic eche processes (electrolyte H2SO4/HClO4/H3PO4 OR solution_ph < 3)
drop table if exists r0survey.acid_proc cascade;
create table r0survey.acid_proc as
select p.id proc_id, pd.technique, pd.parameters->>'electrolyte' electrolyte,
  nullif(pd.parameters->>'solution_ph','none') ph_raw, pd.parameters->>'redox_couple_type' redox
from public_release.process p join public_release.process_detail pd on pd.id=p.process_detail_id
where pd.type='eche' and (pd.parameters->>'electrolyte' ~* 'H2SO4|HClO4|H3PO4'
   or (pd.parameters->>'solution_ph' ~ '^[0-9]' and (pd.parameters->>'solution_ph')::float < 3));
create index on r0survey.acid_proc(proc_id);

-- acidic sample-processes, composition captured once (final else initial)
drop table if exists r0survey.acid_sp cascade;
create table r0survey.acid_sp as
select sp.id sp_id, sp.sample_id, ap.proc_id, ap.technique, ap.electrolyte, ap.ph_raw,
       s.label sample_label, coalesce(s.final_composition, s.initial_composition)::jsonb comp
from public_release.sample_process sp
join r0survey.acid_proc ap on ap.proc_id=sp.process_id
join public_release.sample s on s.id=sp.sample_id;
create index on r0survey.acid_sp(sp_id); create index on r0survey.acid_sp(sample_id);

-- acidic CP overpotential values
drop table if exists r0survey.acid_cp_fom cascade;
create table r0survey.acid_cp_fom as
select a.sample_id, a.sample_label, a.electrolyte, a.ph_raw, a.technique, a.comp,
       (an.output->>'Eta.V_ave')::float eta_v_ave
from r0survey.acid_sp a
join public_release.sample_process_process_data sppd on sppd.sample_process_id=a.sp_id
join public_release.process_data_analysis pda on pda.process_data_id=sppd.process_data_id
join public_release.analysis an on an.id=pda.analysis_id
where a.technique like 'CP%' and an.name='CP_FOMS_standard' and (an.output->>'Eta.V_ave') is not null;
create index on r0survey.acid_cp_fom(sample_id);
-- (see MPS_SURVEY.md for the metal-coverage, distribution, and replicate-floor queries)
