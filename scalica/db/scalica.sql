/* Create our database */
CREATE DATABASE scalica CHARACTER SET utf8;

/* Setup permissions for the server */
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'client';
/*CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'foobarzoot';*/
GRANT ALL ON scalica.* TO 'testuser'@'localhost' IDENTIFIED BY 'client' ;
/*GRANT ALL ON scalica.* TO 'www-data'@'localhost';*/
