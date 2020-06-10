CREATE DATABASE Chat_history;
USE Chat_history;
CREATE TABLE history (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT ,
  username VARCHAR(255) NOT NULL,
  chat VARCHAR(255) ,
  sent_date date);
