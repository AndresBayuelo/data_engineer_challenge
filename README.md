# Data Engineer Challenge

Para levantar los servicios es necesario tener instalado Docker y Docker Compose.

Para levantar los servicios, ejecutar el siguiente comando:

```bash
docker compose build && docker compose up -d
```

Debido a que el servicio de base de datos tarda en levantarse, es necesario esperar unos segundos antes de ejecutar el comando de migración.

```bash
docker exec -it data_engineer_challenge-processing_service-1 python manage.py migrate
```