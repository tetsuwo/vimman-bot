DROP TABLE IF EXISTS myapp.operations;
DROP TABLE IF EXISTS myapp.questions;
DROP TABLE IF EXISTS myapp.answers;
DROP TABLE IF EXISTS myapp.informations;
DROP TABLE IF EXISTS myapp.tweets;
DROP TABLE IF EXISTS myapp.responses;

CREATE TABLE myapp.operations(
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    salt VARCHAR(50),
    state INTEGER,
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE myapp.questions(
    id INTEGER NOT NULL AUTO_INCREMENT,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE myapp.answers(
    id INTEGER NOT NULL AUTO_INCREMENT,
    question_id INTEGER,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE myapp.informations(
    id INTEGER NOT NULL AUTO_INCREMENT,
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE myapp.tweets(
    id INTEGER NOT NULL AUTO_INCREMENT,
    type VARCHAR(10),
    tweet_id INTEGER,
    content TEXT,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE myapp.responses(
    id INTEGER NOT NULL AUTO_INCREMENT,
    type VARCHAR(10),
    content TEXT,
    state INTEGER,
    created_by VARCHAR(50),
    updated_by VARCHAR(50),
    created_at datetime NOT NULL,
    updated_at datetime NOT NULL,
    PRIMARY KEY (id)
);
