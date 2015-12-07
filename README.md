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

# Install Pillow (For file uploads)
```
# Install dependencies
sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

# Install Pillow
pip install -U Pillow
```

* Run
```
./manage.py runserver
```

# Enabling tests in postgresql
1. ALTER USER django CREATEDB;