# Setting the development environment up manually

1. Install MySQL or MariaDB ([Windows](https://mariadb.com/kb/en/installing-mariadb-msi-packages-on-windows/) and create a local database for the project. Both databases come with the MySql workbench.

  Create a new database:
  mysql> CREATE DATABASE databasenamegoeshere CHARACTER SET utf8;
  
  Create a new MySQL user with a password:      
  mysql> CREATE USER ‘username’@‘localhost’ IDENTIFIED BY ‘password’;
  
  Grant the new MySQL user permissions to manipulate the database:      
  * mysql> GRANT ALL PRIVILEGES ON *.* TO 'django'@'localhost'; 'root'@'localhost' in mariadb
        
* Installing mysql on Linux:
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql, if it doesn't work mysql -u root -p, will ask for the mysql root password 
Create a user "django":
mysql> CREATE USER 'django'@'localhost' IDENTIFIED BY 'salasana';

* In case of an error "Access denied for user 'django'@'localhost'.... "


* Add database name, username and your password in the .env file (see below). 

1. Clone the project from the [github repository](https://github.com/IELuomus/extractiontool) with 
```git clone git@github.com:IELuomus/extractiontool.git```

3. `pip install virtualenv`
4. `source venv/bin/activate`

6. Create an .env file (in the folder "project") which contains the following
   `DATABASE_NAME = xxxx` as defined above
   `DATABASE_USER = username` as defined above
   `DATABASE_PASSWORD = password` as defined above
   `DATABASE_HOST=127.0.0.1`
   `DATABASE_PORT=3306`
   `EMAIL_USER=…` according to your email backend
   `EMAIL_PASS=…` according to your email backend


1. In the project root folder (the one where manage.py is) run `pip install -r requirements.txt` (it will take some time).

1. Run `python3 manage.py createsuperuser` 
(always use just `python` in Windows instead of `python3`), and create the credentials when prompted for.
With these superuser credentials you will be able to login to django admin panel at https://127.0.0.1:8000/admin.
1. Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to create the database tables.

1. Go to https://127.0.0.1:8000/admin in your browser, and login with your superuser credentials to set the 
configuration for the Orcid login. Disregard the warning about a missing certificate and find the proper way to bypass this,
depending on your browser (in Chrome click Advanced and then proceed to the destination). The database table "users" is 
required for the Orcid login, so after configuring Orcid, run again `python3 manage.py makemigrations` and `python3 manage.py migrate`.
1. Social account provider: Orcid. Site: modify example.com. Site id must be 1.

