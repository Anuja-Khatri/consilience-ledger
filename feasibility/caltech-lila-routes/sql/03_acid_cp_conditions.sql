-- Join acid CP FOM rows to their process_detail parameters (same path the adapter uses:
-- acid_sp.proc_id = process.id ; process.process_detail_id = process_detail.id).
-- Report the condition fields actually recorded in the process parameters, grouped.
with rows as (
  select f.sample_id, f.electrolyte, f.ph_raw, f.technique, f.eta_v_ave,
         pd.parameters::jsonb as p
  from r0survey.acid_cp_fom f
  join r0survey.acid_sp a on a.sample_id = f.sample_id and a.technique = f.technique
  join public_release.process pr on pr.id = a.proc_id
  join public_release.process_detail pd on pd.id = pr.process_detail_id
  where f.eta_v_ave is not null
    and f.electrolyte in ('H2SO4(aq)','KH2PO4/K2HPO4(aq)')
    and jsonb_typeof(f.comp) = 'object'
)
select electrolyte,
       p->>'concentration' as concentration,
       p->>'solution_ph' as solution_ph,
       p->>'measurement_area' as measurement_area,
       p->>'current_abs' as current_abs,
       p->>'acquisition_time' as acquisition_time,
       p->>'ref_electrode_type' as ref_electrode,
       count(*) as n_rows
from rows
group by electrolyte, concentration, solution_ph, measurement_area, current_abs, acquisition_time, ref_electrode
order by electrolyte, n_rows desc;
