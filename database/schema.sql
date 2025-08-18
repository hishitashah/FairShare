-- 1. Users table (family members)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(20) NOT NULL, -- e.g., 'male', 'female', 'nonbinary', etc.
    email VARCHAR(100) UNIQUE NOT NULL, -- for login
    password_hash VARCHAR(255) NOT NULL, -- for authentication
    relationship VARCHAR(20), -- e.g., 'parent', 'child', 'sibling', etc.
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL -- who added this user (nullable)
);

-- 2. Chores table (types of chores)
CREATE TABLE chores (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50), -- e.g., 'cleaning', 'cooking', etc.
    description TEXT
);

-- 3. Chore Assignments (who is assigned what chore and when)
CREATE TABLE chore_assignments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    chore_id INTEGER REFERENCES chores(id) ON DELETE CASCADE,
    assigned_date DATE NOT NULL,
    due_date DATE
);

-- 4. Chore Logs (who did what, when, and how long)
CREATE TABLE chore_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    chore_id INTEGER REFERENCES chores(id) ON DELETE CASCADE,
    date_completed DATE NOT NULL,
    duration_minutes INTEGER, -- time spent on the chore
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_chore_logs_user_id ON chore_logs(user_id);
CREATE INDEX idx_chore_logs_chore_id ON chore_logs(chore_id);