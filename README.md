# MOB Project #
## Prerequires ##

- python >= 3.6
- pip3
- virtualenv

## Packages ##
Install the required packages:
```bash
sudo apt-get install python3 python3-setuptools python3-dev libevent-dev build-essential python3-pip python3-venv libxml2-dev libxslt1-dev && \
sudo apt-get install python3-mysqldb && \
sudo apt-get install pkg-config libmysqlclient-dev && \
sudo apt-get install libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev liblcms2-dev libwebp-dev
```

**Note:** This codebase was originally written for Python 2.7. While we recommend upgrading to Python 3, the legacy code remains unchanged. See the Installation section below for Python 3 setup.


## Installation ##

### Install Maria DB ###
```bash
sudo apt-get install mariadb-server mariadb-client
sudo mysql_secure_installation
```

Configure the database:
```bash
$ sudo mysql_secure_installation

> Switch to unix_socket authentication [Y/n] n
> Change the root password? [Y/n] Y
> New password: <YOUR_ROOT_DB_PASSWORD>
> Remove anonymous users? [Y/n] Y
> Disallow root login remotely? [Y/n] Y
> Remove test database and access to it? [Y/n] Y
> Reload privilege tables now? [Y/n] Y
```

### Create the database and user ###
```bash
sudo mysql -u root -p
> CREATE DATABASE mob_site CHARACTER SET UTF8;
> CREATE USER 'mob_user'@'localhost' IDENTIFIED BY '<YOUR_DB_PASSWORD>';
> GRANT ALL PRIVILEGES ON mob_site.* TO 'mob_user'@'localhost';
> FLUSH PRIVILEGES;
```

### Import schema
```bash
zcat ~/backups/<YOUR_BACKUP_FILE> | mysql -u 'mob_user' -h localhost -p mob_site
```

### Clone the code ###
```bash
git clone git@github.com:DmitryRendov/mob-site.git
```

### Creating the environment ###
Create a virtual python environment.

#### For Python 3 (Recommended) ####
```bash
python3 -m venv python-bin
source ./python-bin/bin/activate
```

### Install requirements ###

#### For Python 3 ####
```bash
pip3 install -r requirements.txt
pip3 install -r requirements/development.txt
```

**Important:** If you encounter compatibility issues, you may need to:
1. Update Django to a Python 3 compatible version (Django 1.11+)
2. Update other dependencies as needed for Python 3 compatibility

### Configure project ###

Create a local environment file and set `SECRET_KEY`:

```bash
cp .env.example .env
```

Edit `.env` and set a secure value:

```bash
SECRET_KEY='<YOUR_DJANGO_SECRET_KEY>'
```

`python-decouple` reads this value automatically from `.env`.

You can generate a random key, for example:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"
```

### Sync database ###
```bash
python3 manage.py migrate
```

## Running ##
```bash
python3 manage.py runserver 0.0.0.0:8000
```

Open browser to http://127.0.0.1:8000

