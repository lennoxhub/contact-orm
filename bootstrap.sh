#!/usr/bin/env bash
echo "Updating repo"
#apt-get update

echo "Installing debconf utils"
apt-get install debconf-utils -y

echo "Installing pip"
apt-get install -y python-pip

echo "Installing python-dev"
apt-get install python-dev -y

echo "Installing venv"
apt-get install -y python-virtualenv

echo "Installing git"
apt-get install -y git

echo "Preparing MySQL"
apt-get install debconf-utils -y
debconf-set-selections <<< "mysql-server mysql-server/root_password password 1234"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password 1234"

echo "Installing MySQL"
apt-get install mysql-server -y
apt-get install mysql-client -y
apt-get install libmysqlclient-dev -y

echo "Create Databases and tables"
mysql -u root -p1234 -e "CREATE DATABASE contacts_orm"
mysql -u root -p1234 -e "CREATE DATABASE contacts_orm_test"
mysql -u root -p1234 -e "CREATE TABLE contacts_orm.contacts(id INT NOT NULL AUTO_INCREMENT, name VARCHAR(40) NOT NULL, gender VARCHAR(10) NOT NULL, phone VARCHAR(20) NOT NULL, description VARCHAR(60) NOT NULL, PRIMARY KEY ( id ) )"
mysql -u root -p1234 -e "CREATE TABLE contacts_orm_test.contacts(id INT NOT NULL AUTO_INCREMENT, name VARCHAR(40) NOT NULL, gender VARCHAR(10) NOT NULL, phone VARCHAR(20) NOT NULL, description VARCHAR(60) NOT NULL, PRIMARY KEY ( id ) )"

echo "Done."
