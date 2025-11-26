# Run this in MySQL
"""
CREATE TABLE resumes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(50),
  skills TEXT,
  summary TEXT,
  approved BOOLEAN DEFAULT 0
);
"""