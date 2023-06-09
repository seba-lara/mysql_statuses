#!/bin/bash
set -e

echo "======================TISA========================="
echo "========= Instalando Base de Datos MYSQL =========="
echo "==================================================="
echo " "

echo "Estableciendo entorno para la instalacion [1/5]... "
TMP1=$(mktemp -d) || exit 1

# searches for the line number where finish the script and start the tar.gz
SKIP=$(awk '/^__TARFILE_FOLLOWS__/ { print NR + 1; exit 0; }' $0)
#remember our file name
THIS=$(pwd)/$0
# take the tarfile and pipe it into tar
tail -n +${SKIP} ${THIS} | tar -xz -C ${TMP1}

OUT=/var/lib/docker/smap

mkdir -p ${OUT}/mysql_statuses
mkdir -p ${OUT}/mysql_statuses/mysql_db

echo "Copiando archivos al servidor [2/5]... "

cp ${TMP1}/tmp/docker-compose.yml ${OUT}/mysql_statuses/.
cp ${TMP1}/tmp/uninstall.sh ${OUT}/mysql_statuses/.
chmod +x $OUT/mysql_statuses/uninstall.sh

echo "Cargando imagenes de Docker [3/5]... "
docker load < ${TMP1}/tmp/deploy.tar

echo "Levantando contenedores del servicio mysql [4/5]... "
docker-compose -f ${OUT}/mysql_statuses/docker-compose.yml up -d

echo "borrando archivos generados por el instalador [5/5]..."
rm -rf ${TMP1}

exit 0
__TARFILE_FOLLOWS__
