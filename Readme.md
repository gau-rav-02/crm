# NPTECH CRM

## Requirements
- Python
- MySQL

## How to Run
- Create a databse schema (mysql query is given below for understanding.)
- Clone this Repo
- Update your own MySQL username and password in the code
- Run as a normal python program

## Database Schema
```
-- Create the database
CREATE DATABASE nptech_crm;

-- Use the newly created database
USE nptech_crm;

-- Create the 'users' table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    profile_image LONGBLOB,
    first_name VARCHAR(50),
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    contact_no VARCHAR(10),
    email VARCHAR(100) UNIQUE,
    address TEXT
);

-- Create the 'education' table
CREATE TABLE education (
    edu_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    ssc_percentage FLOAT,
    hsc_diploma_percentage FLOAT,
    diploma_stream VARCHAR(50),
    degree_percentage FLOAT,
    degree_stream VARCHAR(50),
    resume LONGBLOB,
    education_type ENUM('HSC','Diploma'),
    degree_status ENUM('Pursuing','Completed'),
    current_year VARCHAR(20),
    completion_year INT,
    last_year_percentage FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create the 'internships' table
CREATE TABLE internships (
    internship_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    role ENUM('Web Development','App Development','Full Stack Development','Backend Development','AIML','Data Analysis','Software Development'),
    duration ENUM('3 months','4 months','5 months','6 months'),
    joining_date DATE,
    ending_date DATE,
    internship_type ENUM('Paid','Unpaid'),
    stipend_amount DECIMAL(10, 2),
    stipend_frequency  ENUM('per month','one-time','per project'),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

```
