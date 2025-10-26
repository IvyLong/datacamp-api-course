-- Database initialization script for PostgreSQL
-- This script will be automatically executed when the PostgreSQL container starts

-- Create the thoughts table
CREATE TABLE IF NOT EXISTS thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    tags JSONB NOT NULL,
    author VARCHAR(100) DEFAULT 'Anonymous',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_thoughts_author ON thoughts(author);
CREATE INDEX IF NOT EXISTS idx_thoughts_timestamp ON thoughts(timestamp);
CREATE INDEX IF NOT EXISTS idx_thoughts_tags ON thoughts USING GIN(tags);

-- Insert some sample data
INSERT INTO thoughts (text, tags, author) VALUES 
    ('Flask with PostgreSQL is powerful!', '["flask", "postgresql", "python"]', 'Course Instructor'),
    ('Docker makes development environments consistent', '["docker", "devops", "development"]', 'DevOps Engineer'),
    ('APIs are the backbone of modern applications', '["api", "architecture", "backend"]', 'API Developer')
ON CONFLICT DO NOTHING;