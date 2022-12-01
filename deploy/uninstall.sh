#!/bin/bash
echo "========= Uninstall MySQL-DB =========="
echo "======================================="
DIA=`date +"%d-%m-%Y"`
HORA=`date +"%H:%M"`
echo "Do you want uninstall mysql? please write [yes/no] and press enter : "
read OPTION 'yes' 'no'
if [[ ${OPTION} == yes ]]; then
  echo "Uninstalling..."
  OUT=/var/lib/docker/smap/mysql_statuses
  docker-compose -f $OUT/docker-compose.yml down
  docker rmi -f si_injectstatus_mysql:latest si_mysql:latest si_adminer:latest
  mv $OUT/mysql_db /root/$DIA_$HORA_mysqldb_backup
  rm -rf /var/lib/docker/smap/mysql_statuses
  rm -rf /tmp/tmp.*
  echo 'Uninstall Completed'
  exit 0
else
  echo "Cancelled"
fi
