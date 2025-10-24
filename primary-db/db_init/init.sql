
    CREATE TABLE IF NOT EXISTS log_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        record_time VARCHAR(75) NOT NULL UNIQUE,
        message VARCHAR(255) NOT NULL,
        hostname VARCHAR(25) NOT NULL,
	command_name VARCHAR(75) NOT NULL,
	process_id INT,
	priority INT NOT NULL,
        syslog_id VARCHAR(15) NOT NULL
    );
