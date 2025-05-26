CREATE TABLE IF NOT EXISTS greedy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT
);

CREATE TABLE IF NOT EXISTS max_flow (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT
);

CREATE TABLE IF NOT EXISTS local_search (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT
);

CREATE TABLE IF NOT EXISTS CP (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT
);

CREATE TABLE IF NOT EXISTS MIP (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT
);

CREATE TABLE IF NOT EXISTS LP    (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_papers INT,
    num_reviewers INT,
    reviews_per_paper INT,
    max_load INT,
    time_execution FLOAT,
    max_load INT    
);



