-- Languages (en/fr)
CREATE TABLE languages (
  id INTEGER PRIMARY KEY,
  lang_code TEXT NOT NULL UNIQUE
);

-- Top-level Places
CREATE TABLE places (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  image TEXT,
  language_id INTEGER NOT NULL REFERENCES languages(id)
);

-- Second-level Sections
CREATE TABLE sections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  place_id INTEGER NOT NULL REFERENCES places(id),
  name TEXT NOT NULL,
  image TEXT
);

-- Third-level Items
CREATE TABLE items (
  id TEXT PRIMARY KEY,
  section_id INTEGER NOT NULL REFERENCES sections(id),
  name TEXT NOT NULL,
  is_not_bold BOOLEAN NOT NULL DEFAULT 0,
  disabled BOOLEAN NOT NULL DEFAULT 0
);

-- Text content under items
CREATE TABLE item_texts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id TEXT NOT NULL REFERENCES items(id),
  html TEXT,
  image TEXT,
  link TEXT
);
