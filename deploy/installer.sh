#!/bin/bash

echo "======================TISA========================="
echo "========= Instalando Base de Datos MYSQL =========="
echo "==================================================="
echo " "

TMP1=$(mktemp -d) || exit 1

# searches for the line number where finish the script and start the tar.gz
SKIP=$(awk '/^__TARFILE_FOLLOWS__/ { print NR + 1; exit 0; }' $0)
#remember our file name
THIS=$(pwd)/$0
# take the tarfile and pipe it into tar
tail -n +${SKIP} ${THIS} | tar -xz -C ${TMP1}

OUT=/var/lib/docker/smap

echo "Copiando archivos al servidor... "
rm -rf ${OUT}/mysql_config
mkdir -p ${OUT}/mysql_config
mkdir -p ${OUT}/mysql_config/mysql_db
cp ${TMP1}/build/mysql_app/docker-compose.yml 

echo " "
docker load ${TMP1}/build/mysql_app/images/deploy.tar

echo -n "borrando archivos generados por el instalador..."
rm -rf ${TMP1}

exit 0
__TARFILE_FOLLOWS__
