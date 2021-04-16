show databases;
create database build_guild;
USE build_guild;
SHOW TABLES;

-- Insert SQL
INSERT INTO user VALUES (1, "faisal@example.com", "Faisal Rasool", "pop" , 0);
INSERT INTO user VALUES (2, "rafey@example.com", "Abdul Rafey", "pop", 0);
INSERT INTO user VALUES (3, "manager@example.com", "Manager 1", "pop", 1);

INSERT INTO buyer VALUES (1, "Hadi Ali", 12345,  null);
INSERT INTO buyer VALUES (2, "Haider Ali", 12346,  null);

INSERT INTO plot("id", "type", "address", "status", "size") VALUES (1, "residential", "first",  "not sold", "7 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (2, "residential", "second", "not sold", "2 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (3, "residential", "third",  "not sold", "5 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (4, "residential", "fourth", "not sold", "5 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (5, "residential", "fifth",  "not sold", "7 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (4, "residential", "sixth",  "not sold", "5 marla");
INSERT INTO plot("id", "type", "address", "status", "size") VALUES (5, "residential", "seventh","not sold", "7 marla");

-- Deleting SQL
DELETE FROM user WHERE id=2;

-- Droping Tables
DROP TABLE transaction;
DROP TABLE deal;
DROP TABLE notes;
DROP TABLE commissionagent;
DROP TABLE buyer;
DROP TABLE plot;
DROP TABLE user;


-- Selecting
SELECT * FROM user;