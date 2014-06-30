# Create tables for tweets collected in 2014.

CREATE TABLE IF NOT EXISTS vaccine.tweets_2014
(
tweet_id BIGINT NOT NULL,
user_id BIGINT,
text varchar(255),
created_at datetime,
PRIMARY KEY (tweet_id)
)
;

CREATE TABLE IF NOT EXISTS vaccine.users_2014
(
user_id BIGINT NOT NULL,
user_name varchar(255),
location varchar(255),
PRIMARY KEY (user_id)
)
;

CREATE TABLE IF NOT EXISTS vaccine.sentiment_score_2014
(
tweet_id BIGINT NOT NULL,
algorithm SMALLINT NOT NULL,
revision VARCHAR(64),
result FLOAT,
PRIMARY KEY (tweet_id, algorithm, revision)
)
;

CREATE TABLE IF NOT EXISTS vaccine.user_locations_2014(
user_id BIGINT,
user_name VARCHAR(64),
quality INT,
latitude FLOAT,
longitude FLOAT,
offsetlat FLOAT,
offsetlon FLOAT,
radius INT,
name VARCHAR(64),
line1 VARCHAR(64),
line2 VARCHAR(64),
line3 VARCHAR(64),
line4 VARCHAR(64),
house VARCHAR(64),
street VARCHAR(64),
xstreet VARCHAR(64),
unittype VARCHAR(64),
unit VARCHAR(64),
postal VARCHAR(64),
neighborhood VARCHAR(64),
city VARCHAR(64),
county VARCHAR(64),
state VARCHAR(64),
country VARCHAR(64), 
countrycode VARCHAR(64),
statecode VARCHAR(64),
countycode VARCHAR(64),
uzip VARCHAR(64),
hash VARCHAR(64),
woeid VARCHAR(64),
woetype VARCHAR(64),
stop_words_count INT,
number_of_results INT,	
PRIMARY KEY (user_id)
)
;

