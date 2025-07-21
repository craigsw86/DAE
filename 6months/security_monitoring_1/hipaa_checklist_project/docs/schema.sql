CREATE TABLE checklist_regulation (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    code VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE checklist_userchecklist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    regulation_id INTEGER REFERENCES checklist_regulation(id),
    completed BOLLEAN DEFAULT FALSE,
    notes TEXT, --Encrypted
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);