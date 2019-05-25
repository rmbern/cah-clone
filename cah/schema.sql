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

-- TODO: Remove id and use rowid?
--       id is redundant, but using large question strings
--       for primary keys is clunky...
CREATE TABLE questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT
);


-- The db is the easiest way to share a single state
-- between all clients, so a db table with only one
-- entry makes sense.
CREATE TABLE current_question (
  question TEXT
);

-- TODO: Move this all into an init script. It does
--       not define a schema.

INSERT INTO questions (question)
  VALUES ("THIS IS A SAMPLE QUESTION");

INSERT INTO questions (question)
  VALUES ('A bald man complained, "My wife thinks my head is an egg! Last night she tried to _________ it.');

INSERT INTO questions (question)
  VALUES('Come enroll at the school of ______!');

INSERT INTO questions (question)
  VALUES('The surgeon said, "The man I''m operating on must be a magician. When I reached in to pull out his appendix, I got a ___________ instead!"');

INSERT INTO questions (question)
  VALUES('The best superpower a hero can have is ________.');

INSERT INTO questions (question)
  VALUES('I''m so hungry, I could eat a ________!');

INSERT INTO questions (question)
  VALUES('What would be a bad job for someone who is accident prone?');

INSERT INTO questions (question)
  VALUES('Name something people are often chased by in movies.');

INSERT INTO questions (question)
  VALUES('Name something you squeeze.');

INSERT INTO questions (question)
  VALUES('Name something you wouldn''t do while people are watching.');

INSERT INTO questions (question)
  VALUES('What does a cow think when the farmer is milking it?');

INSERT INTO questions (question)
  VALUES('Help! I''ve fallen and I can''t ______.');

INSERT INTO questions (question)
  VALUES('Head On! Apply directly to the _______.');

INSERT INTO questions (question)
  VALUES('Name something a death metal band would sing about.');

INSERT INTO questions (question)
  VALUES('Name something that would get you arrested for doing in public.');

INSERT INTO questions (question)
  VALUES('What does Santa Claus really do after he goes down the chimney?');

INSERT INTO questions (question)
  VALUES('What is Clippy doing after being fired from Microsoft Office?');

INSERT INTO questions (question)
  VALUES('Name a bad reason to sell your soul to the devil.');

INSERT INTO questions (question)
  VALUES('What is Eminem going to be rapping about when he''s 80?');

INSERT INTO questions (question)
  VALUES('What is something you can say about your pet but not your significant other?');

INSERT INTO questions (question)
  VALUES('Where is the worst place you could end up after a night of heavy drinking?');

INSERT INTO questions (question)
  VALUES('You get one wish and can''t wish for more wishes. What do you wish for?');

INSERT INTO questions (question)
  VALUES('What does Santa Claus do in the summer?');

INSERT INTO questions (question)
  VALUES('Name something you shouldn''t do while you''re driving.');

INSERT INTO questions (question)
  VALUES('New to the state fair, deep fried _____!');

INSERT INTO questions (question)
  VALUES('What do celebrities normally think about in their dressing room?');

INSERT INTO questions (question)
  VALUES('If aliens visit our planet, what is the first thing we should tell them?');

INSERT INTO questions (question)
  VALUES('What is something you would tell your spouse but not your boss?');

INSERT INTO questions (question)
  VALUES('What does Donald Trump do in his free time?');

-- Start the game off with a random question

-- TODO: Is our random variable uniform in distribution?
INSERT INTO current_question (question)
  VALUES ((SELECT question FROM questions
             WHERE id = (abs(random()) % (SELECT count(*) FROM questions)) + 1));

-- Randomly select a judge using the hidden rowid field sqlite provides.
UPDATE players
SET judge = 1
WHERE rowid = (abs(random()) % (SELECT count(*) FROM players)) + 1;
