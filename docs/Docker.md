# Docker how to

Running this software on your local machine on Docker

## Installing Docker and Docker Compose

- Install Docker
  - OS specific guides can be found: [here](https://docs.docker.com/get-docker/)
- You also need Docker Compose but it's installed with Docker

## Running on your local machine

On your local `.env` file:

```
DATABASE_HOST=db
```

Modify `docker-entrypoint.sh` last line from:
```bash
gunicorn --bind 0.0.0.0:443 --workers ${WORKER_COUNT} project.wsgi:application --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
```
to:
```bash
python3 manage.py runsslserver
```

Also remove from `docker-compose.yml`:
```yml
- type: bind
  source: $HOST/home/cloud-user/certs
  target: /certs
```

And if you have MariaDB/MySQL running on your local machine, you have to stop it, because docker compose tries to initialize one container with MariaDB and tha container uses same port as MySQL/MariaDB service.

### Building the image

On shell/cmd:

```bash
docker-compose build
docker-compose up
```

# ALERT!

When you push to main/deployment, you have to change the last line of `docker-entrypoint.sh` to:

```bash
gunicorn --bind 0.0.0.0:443 --workers ${WORKER_COUNT} project.wsgi:application --certfile /certs/fullchain.pem --keyfile /certs/privkey.pem
```

And add certs bind back:
```yml
volumes:
  - .:/code
  - type: bind
    source: $HOST/home/cloud-user/certs
    target: /certs
```