drop table if exists classes;
CREATE TABLE classes (
  classes_module_code string not null,
  classes_size integer not null,
  classes_room_number string not null,
  classes_time datetime,
  PRIMARY KEY (classes_module_code, classes_time),
  FOREIGN KEY(classes_room_number, classes_time) REFERENCES counts(counts_room_number, counts_time)
);

drop table if exists rooms;
CREATE TABLE rooms (
  rooms_rooms_number string not null,
  rooms_build string not null,
  rooms_campus string not null,
  rooms_capacity integer,
  PRIMARY KEY (rooms_rooms_number),
  FOREIGN KEY (rooms_rooms_number) REFERENCES classes(classes_room_number)
);

drop table if exists counts;
CREATE TABLE counts (
  counts_room_number string not null,
  counts_time datetime,
  counts_module_code string,
  counts_associated integer,
  counts_authenticated integer,
  counts_truth_percent string,
  counts_truth integer,
  PRIMARY KEY (counts_room_number, counts_time)
);