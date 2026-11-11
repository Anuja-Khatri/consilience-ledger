-- Distinct parameter-key sets present on acid CP process_detail rows.
select pd.technique,
       (select string_agg(distinct k, ', ' order by k) from json_object_keys(pd.parameters) k) as param_keys,
       count(*) as n
from public_release.process_detail pd
where pd.technique in ('CP3','CP4')
group by pd.technique, (select string_agg(distinct k, ', ' order by k) from json_object_keys(pd.parameters) k)
order by n desc;
