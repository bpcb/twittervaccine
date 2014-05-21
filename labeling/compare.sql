
drop table if exists vaccine.label_comparison;
create table vaccine.label_comparison(id int, ben_label varchar(1), psu_label varchar(1));

insert into vaccine.label_comparison
select R.id, R.label AS ben_label, case when V.vote='-' then '-' else 'X' end as psu_label
from revised_labels as R, majority_vote_unique AS V
where V.tweet_id = R.id;
