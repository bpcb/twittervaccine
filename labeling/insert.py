#!/usr/bin/env python

"""Publish one or more label files to the database."""

import os
import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection

CREATE_SQL = """
DROP TABLE IF EXISTS revised_labels;
CREATE TABLE revised_labels(id INT, label VARCHAR(1),
  PRIMARY KEY (id))
"""

INSERT_SQL = """
INSERT INTO revised_labels(id, label) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE label=%s;
"""

LABEL_MAP = {'z': '-', 'x': 'X'}

def get_records(philes):
    for phile in philes:
        with open(phile) as fh:
            for line in fh:
                toks = line.split(',')
                yield (int(toks[0]), LABEL_MAP[toks[1].strip()])

if __name__ == '__main__':
    philes = []
    for root, dirs, files in os.walk('.'):
        philes.extend([os.path.join(root, phile) for phile in files
            if phile.startswith('LABELS')])

    conn = get_database_connection(2001)
    cursor = conn.cursor()
    cursor.execute(CREATE_SQL)

    for _id, label in get_records(philes):
        print _id, label
        cursor.execute(INSERT_SQL, [_id, label, label])

    conn.commit()
    cursor.close()
    conn.close()
