# 📊 MySQL Statuses Service

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Area](https://img.shields.io/badge/Area-IoT%20%2F%20Data%20Engineering-orange)

Microservicio Python containerizado que consume mediciones de sensores industriales
desde un broker AMQP, enriquece los datos consultando MongoDB y los persiste
en MySQL en tiempo real. Desarrollado para el proyecto SMAP de monitoreo industrial IoT.

---

## 📌 Caso de uso

> En sistemas IoT industriales donde múltiples sensores publican mediciones
> de forma continua, este servicio actúa como puente entre la mensajería
> en tiempo real (AMQP) y una base de datos relacional (MySQL), permitiendo
> el análisis histórico y la generación de reportes operativos.

---

## ⚙️ ¿Cómo funciona?

1. El servicio se suscribe a la cola `status` del broker AMQP esperando mediciones.
2. Al recibir un mensaje, extrae el campo `key` que identifica al sensor.
3. Consulta MongoDB para obtener la ubicación física del sensor (sector, correa, mesa).
4. Enriquece el mensaje agregando ubicación, timestamp e ID único.
5. Inserta el registro completo en la tabla `statuses` de MySQL.

```
Sensor IoT → AMQP Broker → mysql_statuses → MySQL
                                ↕
                             MongoDB
                          (lookup ubicación)
```

---

## 🚀 Despliegue

**1. Generar el instalador**

```bash
cd deploy/
./deploy.sh
```

Esto genera un archivo autoextraíble `mysql_statuses.run` que contiene
todas las imágenes Docker y archivos de configuración necesarios.

**2. Instalar en el servidor destino**

```bash
./mysql_statuses.run
```

El instalador:
- Extrae las imágenes Docker empaquetadas
- Copia los archivos de configuración a `/var/lib/docker/smap/mysql_statuses`
- Carga las imágenes en Docker
- Levanta los contenedores con Docker Compose

---

## 🛑 Desinstalación

```bash
./uninstall.sh
```

Detiene los contenedores, elimina las imágenes y respalda
la base de datos en `/root/<fecha>_mysqldb_backup` antes de borrar los archivos.

---

## 💻 Uso

```bash
cd src/
pip install -r requirements.txt
python3 main.py
```

> ⚠️ Antes de ejecutar, configura las conexiones a MySQL, AMQP y MongoDB en `main.py`.

---

## 🗂️ Estructura del proyecto

```
mysql_statuses/
│
├── src/
│   ├── main.py              # Servicio principal — lógica de consumo y persistencia
│   ├── sqlHandler.py        # Módulo de conexión y operaciones MySQL
│   ├── amqpHandler.py       # Módulo de conexión y consumo AMQP
│   ├── mongoHandler.py      # Módulo de consultas MongoDB
│   └── requirements.txt     # Dependencias Python
│
├── deploy/
│   ├── deploy.sh            # Script de build y empaquetado
│   ├── installer.sh         # Instalador autoextraíble
│   ├── uninstall.sh         # Script de desinstalación
│   ├── version_info.sh      # Utilidad de versionado Git
│   └── dockerfiles/
│       ├── python/          # Imagen del servicio principal
│       ├── mysql/           # Imagen MySQL 8.0.31
│       └── adminer/         # Imagen Adminer (administración web MySQL)
│
└── README.md
```

---

## 📦 Dependencias

| Paquete | Versión | Descripción |
|---|---|---|
| `pika` | 1.3.1 | Cliente AMQP para RabbitMQ |
| `mysql-connector-python` | 8.0.26 | Conector oficial MySQL |
| `pymongo` | 3.6.0 | Cliente MongoDB |

---

## 🐳 Imágenes Docker

| Imagen | Base | Descripción |
|---|---|---|
| `si_injectstatus_mysql` | python:3.9 | Servicio principal Python |
| `si_mysql` | mysql:8.0.31 | Base de datos MySQL |
| `si_adminer` | adminer:latest | Interfaz web para administración MySQL |

---

## 📨 Estructura del mensaje AMQP

```json
{
  "_id": "uuid generado automáticamente",
  "key": "identificador único del sensor",
  "status": "estado de la medición",
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "idler": "ubicación física del sensor",
  "latch_status": "estado del latch"
}
```

---

## 🛠️ Tecnologías

- **Python 3.9**
- **RabbitMQ** — mensajería AMQP
- **MongoDB** — base de datos de sensores
- **MySQL 8.0.31** — base de datos relacional
- **Docker / Docker Compose**
- **Bash scripting**

---

## 👤 Autor

**Sebastián Lara**
- GitHub: [@seba-lara](https://github.com/seba-lara)

---

## 🏭 Contexto

Este servicio fue desarrollado para el proyecto SMAP, una plataforma IoT
para monitoreo de procesos industriales en sectores minero y forestal.
Los sensores publican mediciones vía AMQP y este servicio las centraliza
en SQL para análisis histórico y reportes operativos.
