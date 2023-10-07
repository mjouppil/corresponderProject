CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(48),
    password TEXT,
    alias VARCHAR(48),
    visible BOOLEAN
);

CREATE TABLE contacts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    contact_id INTEGER REFERENCES users,
    pending BOOLEAN
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(48)
);

CREATE TABLE user_threads (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    message TEXT,
    time TIMESTAMP WITH TIME ZONE
);

CREATE TABLE contact_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    token VARCHAR(24),
    active BOOLEAN
);