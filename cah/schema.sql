DROP TABLE if EXISTS players;
DROP TABLE if EXISTS questions;
DROP TABLE if EXISTS current_question;

CREATE TABLE players (
  name TEXT PRIMARY KEY UNIQUE NOT NULL,
  score INTEGER,
  judge INTEGER,
  ready INTEGER,
  answer TEXT
);

CREATE TABLE questions (
  question TEXT
);

CREATE TABLE current_question (
  question TEXT
);

INSERT INTO questions (question)
  VALUES ("THIS IS A SAMPLE QUESTION");

INSERT INTO current_question (question)
  VALUES ("THIS IS A SAMPLE QUESTION");
