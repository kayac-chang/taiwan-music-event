DROP TABLE IF EXISTS venue_of_event;

DROP TABLE IF EXISTS artists_of_event;

DROP TABLE IF EXISTS event;

DROP TABLE IF EXISTS venue;

DROP TABLE IF EXISTS artist;

CREATE TABLE event (
    id serial PRIMARY KEY,
    title text NOT NULL,
    datetime timestamptz NOT NULL,
    description text
);

CREATE TABLE venue (
    id serial PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE venue_of_event (
    venue_id int REFERENCES venue ON DELETE CASCADE,
    event_id int REFERENCES event ON DELETE CASCADE,
    PRIMARY KEY (venue_id, event_id)
);

CREATE TABLE artist (
    id serial PRIMARY KEY,
    name text NOT NULL UNIQUE
);

CREATE TABLE artists_of_event (
    artist_id int REFERENCES artist ON DELETE CASCADE,
    event_id int REFERENCES event ON DELETE CASCADE,
    PRIMARY KEY (artist_id, event_id)
);

