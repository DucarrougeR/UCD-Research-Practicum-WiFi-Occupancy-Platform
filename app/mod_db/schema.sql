drop table if exists class;
create table class (
  module string primary key not null,
  size integer not null,
  room string not null,
  timeStamp datetime,
  lecture boolean
);

drop table if exists building;
create table building (
  room string not null,
  campus string not null,
  building string not null,
  capacity integer
);

drop table if exists class;
create table class (
  module string primary key not null,
  size integer not null,
  room string not null,
  timeStamp datetime,
  lecture boolean
);