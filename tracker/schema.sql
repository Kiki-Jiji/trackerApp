-- CREATE TABLE user (
--   id TEXT PRIMARY KEY,
--   name TEXT NOT NULL,
--   email TEXT UNIQUE NOT NULL,
--   profile_pic TEXT NOT NULL
-- );

CREATE TABLE Weight (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  weight REAL NOT NULL,
  date TEXT NOT NULL,
  author_id TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
