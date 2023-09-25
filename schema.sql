CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    alias TEXT,
    visibility BOOLEAN
);