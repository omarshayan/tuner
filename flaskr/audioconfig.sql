drop table if exists audioconfig;
create table audioconfig (
  id integer,
  device text,
  driver text,
  PRIMARY KEY (id));
