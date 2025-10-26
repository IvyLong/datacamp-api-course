-- Database initialization script for PostgreSQL
-- This script will be automatically executed when the PostgreSQL container starts

-- Create the thoughts table (Week 3 schema)
CREATE TABLE IF NOT EXISTS thoughts (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'random',
    importance INTEGER DEFAULT 5 CHECK (importance BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_thoughts_category ON thoughts(category);
CREATE INDEX IF NOT EXISTS idx_thoughts_created_at ON thoughts(created_at);
CREATE INDEX IF NOT EXISTS idx_thoughts_importance ON thoughts(importance);

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
INSERT INTO thoughts (text, category, importance) VALUES 
    ('Flask with PostgreSQL is powerful!', 'work', 9),
    ('Docker makes development environments consistent', 'work', 8),
    ('APIs are the backbone of modern applications', 'work', 10),
    ('Learning raw SQL gives you more control', 'personal', 7),
    ('Repository pattern keeps code organized', 'work', 8)
ON CONFLICT DO NOTHING;