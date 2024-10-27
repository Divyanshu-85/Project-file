CREATE DATABASE login_db;

USE login_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(120) NOT NULL
);

-- Insert a sample user for testing
INSERT INTO users (username, password) VALUES ('testuser', 'password123');
