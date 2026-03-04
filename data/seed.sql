DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS aliases;
DROP TABLE IF EXISTS identifiers;
DROP TABLE IF EXISTS incidents;
DROP TABLE IF EXISTS incident_people;

CREATE TABLE people (
  id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  dob TEXT
);

CREATE TABLE aliases (
  person_id INTEGER,
  alias TEXT
);

CREATE TABLE identifiers (
  id INTEGER PRIMARY KEY,
  person_id INTEGER,
  type TEXT,
  value TEXT
);

CREATE TABLE incidents (
  id INTEGER PRIMARY KEY,
  incident_date TEXT,
  description TEXT,
  offense_code TEXT
);

CREATE TABLE incident_people (
  incident_id INTEGER,
  person_id INTEGER,
  role TEXT
);

INSERT INTO people VALUES (1, 'John', 'Smith', '1985-01-05');
INSERT INTO aliases VALUES (1, 'Red');
INSERT INTO identifiers VALUES (1, 1, 'PLATE', 'ABC123');

INSERT INTO incidents VALUES (100, date('now','-10 days'), 'Traffic stop; possible stolen vehicle', 'TS01');
INSERT INTO incident_people VALUES (100, 1, 'SUSPECT');