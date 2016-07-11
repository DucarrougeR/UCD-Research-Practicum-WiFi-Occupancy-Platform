drop table if exists classes;
create table classes (
  classes_module_code string primary key not null,
  classes_size integer primary key not null,
  classes_room_number string not null,
  classes_time datetime
);

drop table if exists rooms;
create table rooms (
  rooms_rooms_number string primary key not null,
  rooms_build string not null,
  rooms_campus string not null,
  rooms_capacity integer
);

drop table if exists counts;
create table counts (
  counts_room_number string primary key not null,
  counts_time datetime primary key,
  counts_module_code string,
  counts_associated integer,
  counts_authenticated integer,
  counts_truth_percent string,
  counts_truth integer
);