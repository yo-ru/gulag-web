# Remove pre-existing tables.
drop table if exists user_sessions;

create table user_sessions
(
  session_id varchar(255) not null primary key,
  user_id int(11) not null,
  login_time timestamp not null
)