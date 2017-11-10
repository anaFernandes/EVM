#!/bin/bash

mkdir -p /opt/mysql  
docker run --name mysql -v /opt/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=pass_ -p 3306:3306 -d mysql
docker run --name phpmyadmin --link mysql:db -p 8080:80 -d phpmyadmin/phpmyadmin   
