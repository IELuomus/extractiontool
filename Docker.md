# Docker how to

Ohje siis miten tämän ohjelmaan saa ajettua omalla koneella Dockerissa

### Alkuaskeleet

- Asenna Docker
  - Järjestelmäkohtaiset ohjeet: [täällä](https://docs.docker.com/get-docker/)
- Tarvitset myös Docker composen, mutta se asentuu Dockerin mukana

### Kun ajetaan lokaalisti

On poistettava Dockerfilestä viimeiset rivit

```
EXPOSE 8080/tcp
CMD ["sh", "-c", "gunicorn --bind :8080 --workers ${WORKER_COUNT} project.wsgi:application"]
```

.env tiedostossa:

```
DATABASE_HOST=db
```

Ja pitää mahdollinen mariadb/mysql service lopettaa omalta koneelta, koska db portti on käytössä

### Imagen buildaaminen

Komentorivillä

```
> docker-compose build
> docker-compose up
```

### Huomioita

Kun Docker ajetaan, ajaa se automaattisesti migraatiot ja käynnistää sslserverin