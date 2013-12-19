drop table if exists todos;
create table todos (
  id integer primary key autoincrement,
  title text not null,
  done integer not null
);