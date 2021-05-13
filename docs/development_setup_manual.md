# Setting the development environment up manually

* Install MySQL or MariaDB  and create a local database for the project. Both databases come with the MySql workbench/CLI.
  
  * Create a new database n the MySql workbench/CLI :
  
  `mysql> CREATE DATABASE databasenamegoeshere CHARACTER SET utf8;`
  
  * In MySql, create a new MySQL user with a password:      
  
  `mysql> CREATE USER ‘username’@‘localhost’ IDENTIFIED BY ‘password’;`
  
  * In MariaDB, a user named 'root' is created as default and with the password given at installation.
  
  * Grant the new MySQL user permissions to manipulate the database:      
  
  `mysql> GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost';`

* Clone the project from the [github repository](https://github.com/IELuomus/extractiontool) with 

`git clone git@github.com:IELuomus/extractiontool.git`

* Create and activate the virtual environment `pip install virtualenv` and `source venv/bin/activate`.

* Create an .env file (in the folder "project") which contains the following

   `DATABASE_NAME = xxxx` as defined above
   
   `DATABASE_USER = username` as defined above
   
   `DATABASE_PASSWORD = password` as defined above
   
   `DATABASE_HOST=127.0.0.1`
   
   `DATABASE_PORT=3306`
   
   `EMAIL_USER xxxx` according to your email backend
   
   `EMAIL_PASS= xxxx` according to your email backend
   
   `DEBUG = True` to show the Django debug toolbar in your browser

* Run `pip install -r requirements.txt` in the project root folder (where manage.py is).

* Run `python3 manage.py createsuperuser`, and create the credentials when prompted for.
With these superuser credentials you will be able to login to django admin panel at https://127.0.0.1:8000/admin.

* Go to https://127.0.0.1:8000/admin in your browser, and login with your superuser credentials to set the 
configuration for the Orcid login. Disregard the warning about a missing certificate and find the proper way to bypass this,
depending on your browser (in Chrome click Advanced and then proceed to the destination). The database table "users" is 
required for the Orcid login, so after configuring Orcid, run again `python3 manage.py makemigrations` and `python3 manage.py migrate`.

Navigate to Social applications --> Add social application and choose Orcid from the dropdown menu. 
Click on the default example.com to modify it. Set https://etie.helsinki.fi as url and ETIE domain name.
Set Client id and Secret key according to those provided by [Orcid devtools setup](https://github.com/IELuomus/extractiontool/blob/main/docs/orcid_setup.md).
Move the site url from 'Available sites' to 'Chosen sites'. 

* Run `python3 manage.py makemigrations` and `python3 manage.py migrate` to create the database tables.


