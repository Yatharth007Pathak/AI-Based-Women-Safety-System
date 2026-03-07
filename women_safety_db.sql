-- AI-Based Women Safety Analytics System
-- Database Schema

-- Create Database
CREATE DATABASE IF NOT EXISTS women_safety_db;
USE women_safety_db;

-- USERS TABLE
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster login lookup
CREATE INDEX idx_users_email ON users(email);

-- EMERGENCY CONTACTS TABLE
CREATE TABLE IF NOT EXISTS emergency_contacts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    relationship VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_emergency_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_emergency_user ON emergency_contacts(user_id);

-- ALERT LOGS TABLE
CREATE TABLE IF NOT EXISTS alert_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    risk_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_alert_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_alert_user ON alert_logs(user_id);
CREATE INDEX idx_alert_time ON alert_logs(created_at);

-- CRIME DATA TABLE
CREATE TABLE IF NOT EXISTS crime_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    crime_type VARCHAR(100),
    risk_score INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_crime_location ON crime_data(latitude, longitude);
CREATE INDEX idx_crime_risk ON crime_data(risk_score);

-- SAMPLE DATA (Optional Testing)

-- Insert sample crime hotspots (replace with real dataset)
INSERT INTO crime_data (latitude, longitude, crime_type, risk_score)
VALUES
(28.6139, 77.2090, 'Harassment', 85),
(28.7041, 77.1025, 'Assault', 78),
(28.5355, 77.3910, 'Theft', 60);

-- END OF SCHEMA