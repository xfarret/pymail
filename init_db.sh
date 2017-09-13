#!/bin/bash
cd database
sqlite3 emails.db "create table aTable(field1 int); drop table aTable;"
cd ..
python manage.py version_control
python manage.py upgrade