# jcrel-ims
Inventory Management System

# Get the app working locally (Ubuntu)
* Clone the repository
```
git clone https://github.com/roselleebarle04/jcrel-ims.git
```

* Create and activate virtualenv
```
virtualenv ~/.envs/jcrel
source ~/.envs/jcrel/bin/activate
```

* Install Requirements 

Note: Install and setup PostgreSQL beforehand. Here's how.  (https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)
```
pip install -r requirements.txt
```

* Run
```
./manage.py runserver
```
