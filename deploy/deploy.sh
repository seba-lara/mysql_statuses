#!/bin/bash


## SET VARIABLES
echo "Estableciendo variables de entorno [1/8]..."
PROJECT=mysql_statuses
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILD_DEST=./tmp
SRC_DIR=./../src
rm -rf ${BUILD_DEST}
VERSION=$(sh version_info.sh -d ${DIR}/.. | \
    sed s/@/_/ | \
    sed s/+/-/g)
TAG=$(echo $VERSION | sed s/-.*/-/g)
NAME=${PROJECT}
IMAGES=""
mkdir -p ${BUILD_DEST}/app

## COPY FILES
cp dockerfiles/python/Dockerfile ${BUILD_DEST}/.
cp ../mysql-conf/docker-compose.yml ${BUILD_DEST}/.
cp uninstall.sh ${BUILD_DEST}/.
cp ${SRC_DIR}/* ${BUILD_DEST}/app/.

## BUILD MYSQL IMAGE
echo "Construyendo imagen de MySQL [2/8]..."
docker build -t si_mysql:latest $DIR/dockerfiles/mysql/
IMAGES+="si_mysql:latest "

## BUILD ADMINER IMAGE
echo "Construyendo imagen de Adminer [3/8]..."
docker build -t si_adminer:latest $DIR/dockerfiles/adminer/
IMAGES+="si_adminer:latest "

## BUILD DOCKER IMAGE FROM DOCKERFILE
echo "Construyendo imagen de Python [4/8]"
docker build -t si_injectstatus_mysql:latest ${BUILD_DEST}/
IMAGES+="si_injectstatus_mysql:latest "

## SAVE DOCKER IMAGES
echo -n "Guardando imágenes de Docker [5/8]... "
docker save ${IMAGES} > $BUILD_DEST/deploy.tar
echo "Ok."

## MAKE INSTALLER
echo -n "Guardando Tar [6/8]..."
tar czf ${NAME}.tar.gz ${BUILD_DEST}
echo "Ok."

echo -n "Generando archivo RUN [7/8]..."
cat installer.sh ${NAME}.tar.gz > ${NAME}.run
chmod +x ${NAME}.run
rm -rf ${NAME}.tar.gz
echo "Ok."

echo -n "Eliminando carpetas temporales [8/8]..."
rm -rf ${BUILD_DEST}
docker rmi -f $IMAGES
echo "Ok."

echo "Deploy generado exitosamente!"
