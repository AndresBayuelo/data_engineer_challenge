# Data Engineer Challenge

## Arquitectura



## Despliegue

Para levantar los servicios es necesario tener instalado Docker y Docker Compose.

Para levantar los servicios, ejecutar el siguiente comando:

```bash
docker compose build && docker compose up -d
```

Debido a que el servicio de base de datos tarda en levantarse, es necesario esperar unos segundos antes de ejecutar el comando de migración.

```bash
docker exec -it data_engineer_challenge-processing-service-1 python manage.py migrate
```

Para visualizar el log de los servicios, ejecutar los siguientes comandos en terminales separadas:

```bash
docker logs -f data_engineer_challenge-reception-service-1
docker logs -f data_engineer_challenge-processing-service-1
```

## Pasos parar probar

En el directorio local se dispone de colección de postman en el directorio `assets/data-engineer-challenge.postman_collection.json` para probar los servicios.

1. Inicialmente, se recomienda ejecutar el endpoint `upload-csv` para enviar un archivo CSV (puede tomar como ejemplo el archivo ubicado en el directorio `assets/coordenates.csv`) para su procesamiento. A continuación, se muestra un ejemplo de la estructura del archivo CSV:

```csv
lat|lon
''52,923454''|''-1,474217''
''53,457321''|''-2,262773''
''50,871446''|''-0,729985''
''50,215687''|''-5,191573''
''57,540178''|''-3,758607''
''nan''|''nan''
```

2. Posteriormente, puede verificar el estado del procesamiento del archivo de las coordenadas con el endpoint `file-detail`.

3. Finalmente, puede consultar la información de las coordenadas procesadas en la tabla `coordinates` conectándose a la instancia de la base de datos con las credenciales que se muestran a continuación.

```env
HOST: localhost
PORT: 5432
USER: postalcodes_user
DB: postalcodes_db
PASSWORD: postalcodes_password
```

4. Si visualiza que no se han procesado todas las coordenadas, puede hacer uso del endpoint `file-reprocess` para seguir el procesamiento del archivo. Lo anterior debido a que la API cuenta con un límite de procesamiento de 20 registros por día.