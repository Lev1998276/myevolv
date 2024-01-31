-- Replace the placeholders with appropriate data types and constraints


-- Replace the placeholder values with your actual data
CREATE OR REPLACE TABLE dlake.choice.api_credentials (
    table_name VARCHAR(255),
    api_name VARCHAR,
    loginname VARCHAR(255),
    password VARCHAR(255)
);


-- Replace the placeholder values with your actual data

INSERT INTO dlake.choice.api_credentials (TABLE_NAME,api_name, loginname, password)
VALUES
    ('HOSPITALIZATION', 'https://myevolvvnshealthdev.netsmartcloud.com/api/session/authenticate', 'apiuser3', 'abc123'),
    ('DUMMY1', 'api2', 'user2', 'password2'),
    ('DUMMY2', 'api3', 'user3', 'password3');
	
	
	loginname = "apiuser3"
password = "abc123"