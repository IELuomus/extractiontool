# Setting the development environment up manually

1. Clone the project from the [github repository](https://github.com/IELuomus/extractiontool) with 
```git clone git@github.com:IELuomus/extractiontool.git```

1. In the project root folder (the one where manage.py is) run `pip install -r requirements.txt` (it will take some time).
1. Create a .env -file in the folder "project" following !this! model.
1. Install MariaDB (not in MacOS?) or MySql and create a local database. Add the username (in MariaDB it is usually "root), 
your password, and the name  of the local database in the .env file. Both databases come with the MySql workbench, 
which can be used to inspect the database.
Installing MariaDB on Windows:
* https://mariadb.com/kb/en/installing-mariadb-msi-packages-on-windows/
* Mariadb will create a default user "root" 

* Installing mysql on Linux:
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql, if it doesn't work mysql -u root -p, will ask for the mysql root password 
Create a user "django":
mysql> CREATE USER 'django'@'localhost' IDENTIFIED BY 'salasana';

When MariaDB / MySql has been installed, in the mysql workbench:

* mysql> CREATE DATABASE ieluomus;
* mysql> GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost';

1. Run, again in the project root folder where manage.py is, `python3 manage.py createsuperuser` 
(always use just `python` in Windows instead of `python3`), and create the credentials when prompted for.
With these superuser credentials you will be able to login to django admin panel at https://127.0.0.1:8000/admin.
1. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to create the database tables.
1. Start the server with `python manage.py runsslserver`. The sslserver is required by the Orcid login (see below).
1. Go to https://127.0.0.1:8000/admin in your browser, and login with your superuser credentials to set the 
configuration for the Orcid login. Disregard the warning about a missing certificate and find the proper way to bypass this,
depending on your browser (in Chrome click Advanced and then proceed to the destination). The database table "users" is 
required for the Orcid login, so after configuring Orcid, run again `python3 manage.py makemigrations` and `python3 manage.py migrate`.
1. Social account provider: Orcid. Site: modify example.com. Site id must be 1.

