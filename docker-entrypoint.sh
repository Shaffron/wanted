#!/bin/bash

# wait for mysql running
dockerize -wait tcp://mysql:3306 -timeout 20s

service mysql start

echo "Create database schema"
mysql -h mysql -u root -e "CREATE DATABASE wanted CHARACTER SET utf8 COLLATE utf8_general_ci"

echo "Initialize database"
python db.py db init
python db.py db migrate
python db.py db upgrade

echo "Immigrate csv test data to database"
python db.py immigrate

echo "Start flask server"
python run.py