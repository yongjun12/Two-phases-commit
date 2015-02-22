#!/bin/bash

sqlite3 ex <<SQL_ENTRY_TAG_1
create table if not exists log(operate_id integer, server varchar(30));
create table if not exists info(key varchar(20) unique, value varchar(20));
SQL_ENTRY_TAG_1

