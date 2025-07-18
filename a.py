import json
import sqlite3

# Load JSON from local file
with open("a.json", "r", encoding="utf-8") as f:
    data = json.load(f)

conn = sqlite3.connect("places.sqlite")
cur = conn.cursor()

# Drop and recreate tables
cur.executescript("""
DROP TABLE IF EXISTS item_texts;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS languages;

CREATE TABLE languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang_code TEXT NOT NULL UNIQUE
);

CREATE TABLE places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT,
    language_id INTEGER NOT NULL
);

CREATE TABLE sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    image TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT,
    section_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    is_not_bold BOOLEAN DEFAULT 0,
    disabled BOOLEAN DEFAULT 0
);

CREATE TABLE item_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    html TEXT,
    image TEXT,
    link TEXT
);
""")

conn.execute("BEGIN")
cur.executemany("INSERT INTO languages (lang_code) VALUES (?)", [("en",), ("fr",)])
lang_map = {row[0]: row[1] for row in cur.execute("SELECT lang_code, id FROM languages")}

for lang in ["en", "fr"]:
    for place in data[lang]:
        cur.execute("INSERT INTO places (name, image, language_id) VALUES (?, ?, ?)",
                    (place["name"], place.get("image"), lang_map[lang]))
        place_id = cur.lastrowid

        for section in place["data"]["children"]:
            cur.execute("INSERT INTO sections (place_id, name, image) VALUES (?, ?, ?)",
                        (place_id, section["name"], section.get("image")))
            section_id = cur.lastrowid

            for item in section["data"]["children"]:
                cur.execute("""INSERT INTO items (item_id, section_id, name, is_not_bold, disabled)
                               VALUES (?, ?, ?, ?, ?)""",
                            (
                                item["id"],
                                section_id,
                                item["name"],
                                bool(item.get("isNotBold", False)),
                                bool(item.get("disabled", False))
                            ))
                db_item_id = cur.lastrowid

                for text in item.get("data", {}).get("text", []):
                    cur.execute("""INSERT INTO item_texts (item_id, html, image, link)
                                   VALUES (?, ?, ?, ?)""",
                                (db_item_id, text.get("html"), text.get("image"), str(text.get("link"))))

conn.commit()
conn.close()
print("✅ Successfully built 'places.db' from local a.json")
