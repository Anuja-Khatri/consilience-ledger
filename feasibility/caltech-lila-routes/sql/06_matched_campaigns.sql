-- Campaign attribution for matched DB samples (t=0.05): plate (collection label) + plate DOI.
select c.label as plate, c.doi as plate_doi, count(distinct cs.sample_id) as n_matched_samples
from public_release.collection__sample cs
join public_release.collection c on c.id=cs.collection_id
where cs.sample_id = any(string_to_array(:'ids',',')::uuid[])
group by c.label, c.doi
order by n_matched_samples desc
limit 25;
