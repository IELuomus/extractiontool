# POUTA documentation

Pouta is a general purpose VPS (Virtual Private Server) provided by CSC.

Sections marked with * assumes that you have logged in to Pouta SSH.

## General idea how Pouta environment works

Pouta is configured to run docker and docker-compose. The application runs on one docker container and database runs on another container. Port 3306 is used by the database and port 443 (https) is used by the application container. Also ports 80 and 8000 (http) are reserved to the application container. 

These containers are configured with docker-compose and you can find used file on the repository root named `docker-compose.yml`. Docker-compose builds the application based on the Dockerfile found on the repository root.

Pouta is configured to utilize webhook. By calling this hook Pouta downlaods the newest version of application sourcecode from `deployment` branch. After that Pouta builds the new application container and replaces the old one. Hooks URL is `http://etie.it.helsinki.fi:9000/hooks/redeploy`. This hook has a secret, and the hook will not be ran if the secret is not provided.

Pouta runs on CentOS 8, so if you want to install something, you'll need to use `yum` and `dnf`. The application sourcecode can be found in Pouta on `~/web/tool`

## How to connect to Pouta

You need SSH key to log in to Pouta. In your local machine you'll need to have the private SSH key and the corresponding public key needs to be in Pouta's configuration files.

Your private SSH key has to be read only. Pouta will not grant access, if the keyfile has some other rules. To make your key read only, run this command (linux): `chmod 0444 <keyfile>`

You can log in to Pouta with this bash line:
```bash
ssh <user-name>@etie.it.helsinki.fi -i <keyfile>
```

If Pouta doesn't have your public key listed and you have a good reason to access Pouta, please contact one of the repository admins.

## * Editing Pouta configuration

### Adding new SSH keys to Pouta's configuration

Get the public key you want to add to Poutas configuration and copy/paste it to a new line in file: `~/.ssh/authorized_keys`

### Editing webhook

Webhook runs on supervisord. More of supervisord's documentation can be found [here.](http://supervisord.org/) Configuration of supervisord regarding to webhook is at the bottom of `/etc/supervisord.conf`. And the log file of webhooks output by supervisord is on `~/hooks/supervisor.log`

The webhook configuration file is in `~/web/hooks.json`. This file has the basic webhook configuration (secret, command to execute, id). The webhook executes `~/web/redeploy.sh` script that is used to pull from github and runs docker commands. So if you want to modify what redeploy hook does, modify the `redeploy.sh` file.

### Firewall

Pouta is configured to use firewalld. For further reading, follow [this link.](https://firewalld.org/documentation/man-pages/firewall-cmd.html)

The firewall is configured to allow trafic from specific ports, eg. 443 (https) and 22 (SSH). Used zone of firewalld is `public`