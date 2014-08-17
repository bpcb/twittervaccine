// Calculate fraction of users with location information in 2014
select count(*) from users_2014;
// 247,869
select count(*) from users_2014 where location != '';
// 172,644
// 69.7%

// Number of users with GPS coordinates in their location tags.
select count(*) from users_2014 where location regexp '[0-9][0-9].[0-9][0-9][0-9][0-9][0-9][0-9]'
// 1374