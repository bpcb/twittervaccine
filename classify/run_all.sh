#!/bin/sh

mysql -uroot < count_votes.sql
mysql -uroot < total_votes.sql
#mysql -uroot < vote_fraction.sql
