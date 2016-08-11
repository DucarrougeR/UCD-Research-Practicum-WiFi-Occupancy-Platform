drop table if exists classes;
CREATE TABLE classes (
  classes_room_number VARCAHR(5) not null,
  classes_time datetime,
  classes_module_code VARCHAR(10) not null,
  classes_size integer not null,
  classes_attendance_score integer, 
  PRIMARY KEY (classes_module_code, classes_time),
  FOREIGN KEY(classes_room_number, classes_time) REFERENCES counts(counts_room_number, counts_time)
);

drop table if exists rooms;
CREATE TABLE rooms (
  rooms_rooms_number VARCAHR(5) not null,
  rooms_building VARCHAR(20) not null,
  rooms_campus VARCHAR(20) not null,
  rooms_capacity integer,
  room_occupancy_score integer,
  PRIMARY KEY (rooms_rooms_number),
  FOREIGN KEY (rooms_rooms_number) REFERENCES classes(classes_room_number)
);

drop table if exists counts;
CREATE TABLE counts (
  counts_room_number VARCHAR(5) not null,
  counts_truth_percent VARCHAR(4),
  counts_truth integer,
  counts_module_code VARCHAR(10),
  counts_time datetime,
  counts_associated integer,
  counts_authenticated integer,
  counts_truth_is_occupied integer,
  counts_predicted integer,
  counts_predicted_is_occupied integer,
  PRIMARY KEY (counts_room_number, counts_time)
);