# Docker how to

Running this software on your local machine on Docker

## Installing Docker and Docker Compose

### Install Docker
  - OS specific guides can be found: [here](https://docs.docker.com/get-docker/)
- You also need Docker Compose but it's installed with Docker

#### Install Docker on Ubuntu 20.04 with script:

-  `bash devscripts/ubuntu/install_docker.sh`

## Running on your local machine
- have `.env` in `extractiontool/` root  
( check `devscripts/.env-file-example` )  

Note: If you have MariaDB/MySQL running on your local machine, you have to stop it, because docker compose tries to initialize one container with MariaDB and that container uses same port as MySQL/MariaDB service. Linux and macOS run-scripts try to stop possible MariaDB/MySQL service.  

### Linux
- `bash devscripts/run_docker.sh`

### Windows
- `devscripts/windows/run_windows_docker.bat`

### macOS
- `bash devscripts/darwin/run_macOS_docker.sh`

Script will setup everything ready to start developing. Two local super-users are created using the value in the variables  
`$DJANGO_SUPERUSER_USERNAME`  
`$DJANGO_SUPERUSER_PASSWORD`  
`$DJANGO_SUPERUSER_EMAIL`  
, the second one with just number `2` added to the end for all.

NOTE: Windows and macOS GUI:sh have a bug which makes running/stopping Docker from the graphical user interface to cause an error. Solution is to just start and stop from the commandline until Docker-developers fix the bug. https://github.com/docker/for-win/issues/9539
