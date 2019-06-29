CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(126) UNIQUE,
    handle VARCHAR(126),
    password CHAR(60)
);


CREATE TABLE authors (
 id SERIAL PRIMARY KEY,
name VARCHAR(63) UNIQUE
);


CREATE TABLE books(
id SERIAL PRIMARY KEY,
title VARCHAR(63),
author_id INTEGER REFERENCES authors(id),
isbn CHAR(10) UNIQUE,
year CHAR(4),
tsv tsvector
);

CREATE INDEX ix_books_tsv ON books USING GIN(tsv);

