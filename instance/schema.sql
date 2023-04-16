CREATE TABLE ACCOUNT
(
    account_id integer PRIMARY KEY AUTOINCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    isActive boolean NOT NULL DEFAULT true
);

CREATE TABLE ROLE
(
    role_id integer PRIMARY KEY AUTOINCREMENT,
    role_name varchar(255) NOT NULL
);

CREATE TABLE ACCOUNT_ROLE
(
    account_id integer,
    role_id integer,
    PRIMARY KEY (account_id, role_id),
    FOREIGN KEY (account_id) REFERENCES ACCOUNT (account_id),
    FOREIGN KEY (role_id) REFERENCES ROLE (role_id)
);

CREATE TABLE APPLICATION
(
    id integer PRIMARY KEY AUTOINCREMENT,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    email varchar(255) NOT NULL,
    start_date date NOT NULL,
    occupation varchar(255) NOT NULL,
    accepted boolean NOT NULL
);

INSERT INTO ROLE (role_name) values ("Admin"), ("User");
