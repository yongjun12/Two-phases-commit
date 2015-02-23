# Setup Database on server/coordinator 
# Log: log inclusive key fetch
# LogEx: log exclusive key update/delete action
# Info: store value. Column key acts as a identifier, is always set to be 'key' 

sqlite3 server <<SQL_ENTRY_TAG_1
create table if not exists log(operate_id integer, server varchar(30));
create table if not exists logEx(operate_id integer, server varchar(30));
create table if not exists info(key varchar(20) unique, value varchar(20));
SQL_ENTRY_TAG_1