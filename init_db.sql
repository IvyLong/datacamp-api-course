-- Database initialization script for PostgreSQL
-- This script will be automatically executed when the PostgreSQL container starts

-- Create the thoughts table (Week 3 schema)
CREATE TABLE IF NOT EXISTS thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    tags TEXT[], -- Array of tags
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_thoughts_created_at ON thoughts(created_at);
CREATE INDEX IF NOT EXISTS idx_thoughts_tags ON thoughts USING GIN(tags);

-- Create trigger to automatically update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_thoughts_updated_at ON thoughts;
CREATE TRIGGER update_thoughts_updated_at
    BEFORE UPDATE ON thoughts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Insert some sample data
INSERT INTO thoughts (text, tags) VALUES 
    ('Flask with PostgreSQL is powerful!', ARRAY['work', 'programming']),
    ('Docker makes development environments consistent', ARRAY['work', 'devops']),
    ('APIs are the backbone of modern applications', ARRAY['work', 'api']),
    ('Learning raw SQL gives you more control', ARRAY['personal', 'learning']),
    ('Repository pattern keeps code organized', ARRAY['work', 'architecture'])
ON CONFLICT DO NOTHING;