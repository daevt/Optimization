CREATE TABLE IF NOT EXISTS greedy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);

CREATE TABLE IF NOT EXISTS max_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);

CREATE TABLE IF NOT EXISTS local_search (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);

CREATE TABLE IF NOT EXISTS CP (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);

CREATE TABLE IF NOT EXISTS MIP (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);

CREATE TABLE IF NOT EXISTS LP (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_papers INTEGER,
    num_reviewers INTEGER,
    reviews_per_paper INTEGER,
    max_load INTEGER,
    time_execution FLOAT
);



