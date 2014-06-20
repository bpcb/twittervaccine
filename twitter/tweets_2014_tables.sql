# Create tables for tweets collected in 2014.

CREATE TABLE vaccine.tweets_2014
(
id int NOT NULL AUTO_INCREMENT,
tweet_id int,
user_id int,
text varchar(255),
created_at datetime,
PRIMARY KEY (id)
)
;

CREATE TABLE vaccine.users_2014
(
id int NOT NULL AUTO_INCREMENT,
user_id int,
user_name varchar(255),
location varchar(255),
PRIMARY KEY (id)
)
;

