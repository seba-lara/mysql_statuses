#!/bin/bash

## SET VARIABLES
echo "Creando variables de entorno"
PROJECT=mysql_app
SRC_DIR=${DIR}../src/
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BUILD_DEST=${DIR}/build
rm -rf ${BUILD_DEST}
VERSION=$(sh ${DIR}/version_info.sh -d ${DIR}/.. | \
    sed s/@/_/ | \
    sed s/+/-/g)
TAG=$(echo $VERSION | sed s/-.*/-/g)
NAME=${PROJECT}
IMAGES=""

mkdir -p ${BUILD_DEST}/images
cp ${DIR}/installer.sh ${BUILD_DEST}/installer.sh
cp ${DIR}/../mysql-conf/docker-compose.yml ${BUILD_DEST}/${PROJECT}/docker-compose.yml

## BUILD MYSQL IMAGE
echo "Construyendo imagen de MySQL"
docker pull mysql:latest
IMAGES=+"si_mysql_:${TAG} si_mysql:latest"

## BUILD ADMINER IMAGE
echo "Construyendo imagen de Adminer"
docker pull adminer:4.8.1
IMAGES=+"si_adminer:4.8.1 si_adminer:latest"

## BUILD DOCKER IMAGE FROM DOCKERFILE
echo "Construyendo imagen de Python"
OUT_=${BUILD_DEST}/python_mysql
rm -rf ${OUT_}
mkdir -p ${OUT_}

cp ${SRC_DIR}/main.py ${OUT_}/
cp ${SRC_DIR}/sql_handler.py ${OUT_}/
cp ${SRC_DIR}/amqp_handler.py ${OUT_}/
cp ${DIR}/../requirements.txt ${OUT_}/

docker build -t si_python:${TAG} -t si_python:latest ${DIR}/
IMAGES+="si_python:${TAG} si_python:latest"

## Copy file/s
echo "Copiando archivos"
cp ${DIR}/../docker-compose.yml ${BUILD_DEST}/.

## SAVE DOCKER IMAGES
echo -n "Guardando imágen de Docker..."
docker save ${IMAGES} > ${BUILD_DEST}/${PROJECT}/images/deploy.tar
echo "Ok."

## MAKE INSTALLER
echo -n "Guardando Tar..."
tar czf ${NAME}.tar.gz ${BUILD_DEST}/${PROJECT}
echo "Ok."
echo -n "Eliminando carpetas temporales..."
rm -r ${BUILD_DEST}
echo "Ok."
echo -n "Generando archivo RUN..."
cat installer.sh ${NAME}.tar.gz > ${NAME}.run
chmod +x ${NAME}.run
rm -rf ${NAME}.tar.gz
echo "Ok."
echo "Deploy generado exitosamente"
