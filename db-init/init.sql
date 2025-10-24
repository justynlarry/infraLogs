    CREATE DATABASE IF NOT EXISTS infralogDb01;
    USE infralogDb01;

    CREATE TABLE IF NOT EXISTS  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        record_time VARCHAR(75) NOT NULL UNIQUE,
        message VARCHAR(255) NOT NULL,
        hostname VARCHAR(25) NOT NULL,
	command_name VARCHAR(75) NOT NULL,
	process_id INT(15),
	priority INT(2) NOT NULL,
        syslog_id VARCHAR(15)
    );
