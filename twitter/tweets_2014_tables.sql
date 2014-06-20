# Create tables for tweets collected in 2014.

CREATE TABLE vaccine.tweets_2014
(
tweet_id BIGINT NOT NULL,
user_id BIGINT,
text varchar(255),
created_at datetime,
PRIMARY KEY (tweet_id)
)
;

CREATE TABLE vaccine.users_2014
(
user_id BIGINT NOT NULL,
user_name varchar(255),
location varchar(255),
PRIMARY KEY (user_id)
)
;

