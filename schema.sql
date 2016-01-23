drop table if exists notes;
create table notes (
  id integer primary key autoincrement,
  text text not null
);

/*
 * Sample entries
 */
insert into notes (text) values ('
	This is a fancy note.
');
insert into notes (text) values ('
	This is an even more fancy note. Are you mad bro?
	What happens if we add new lines?
');
