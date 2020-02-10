CREATE TABLE IF NOT EXISTS servidordecorreo(
  id int unsigned not null primary key auto_increment,
  servidor varchar(100) not null default ""
);
INSERT INTO servidordecorreo VALUES(1,"hushmail");

CREATE TABLE IF NOT EXISTS emails (
  id int unsigned not null primary key auto_increment,
  nombre varchar(100) not null default '',
  email varchar(100) not null default '',
  idservidor int unsigned not null default 1,
  password varchar(100) not null default '',
  hasinstagram tinyint(1) not null default 0,
  hasfacebook tinyint(1) not null default 0,
  hastwitter tinyint(1) not null default 0,
  hasyoutube tinyint(1) not null default 0,
  hasalias tinyint(1) not null default 0,
  errors tinyint(2) not null default 0,
  istemp tinyint(1) not null default 0,
  FOREIGN KEY (idservidor) REFERENCES servidordecorreo(id)
);
INSERT INTO emails(nombre,email,password) VALUES("Edens skipp","edens0hulk@hushmail.com","edens.123.321");

CREATE TABLE IF NOT EXISTS alias(
  id int unsigned not null primary key auto_increment,
  idemail int unsigned not null default 1,
  alias varchar(100) not null default "",
  /*

  */
  hasinstagram tinyint(1) not null default 0,
  hasfacebook tinyint(1) not null default 0,
  hastwitter tinyint(1) not null default 0,
  hasyoutube tinyint(1) not null default 0,
  errors tinyint(2) not null default 0,
  istemp tinyint(1) not null default 0,
  FOREIGN KEY (idemail) REFERENCES emails(id)
);

CREATE TABLE IF NOT EXISTS instagram(
  id int unsigned not null primary key auto_increment,
  username varchar(100) not null default "",
  password varchar(100) not null default "",
  /*
    created by
    0 = email,
    1 = alias
  */
  createdby tinyint(1) not null default 0,
  /*
    usedby
    id del email o alias.
  */
  usedby int unsigned not null default 1
);
