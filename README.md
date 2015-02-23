# MOB Project #
## Prerequires ##

- python >= 2.7
- pip
- virtualenv

## Packages ##
sudo apt-get install python-setuptools python-dev libevent-dev build-essential python-pip python-virtualenv libxml2-dev libxslt1-dev
sudo apt-get install python-mysqldb
sudo apt-get install libmysqlclient-dev


## Installation ##
### Creating the environment ###
Create a virtual python environment for the project.
If you're not using virtualenv you may skip this step.

#### For virtualenv ####
```bash
virtualenv python-bin
source ./python-bin/bin/activate
```

### Clone the code ###
Obtain the url to your git repository.

```bash
git clone <URL_TO_GIT_RESPOSITORY> public_html
```

### Install requirements ###
```bash
cd public_html
pip install -r requirements.txt
pip install -r requirements/development.txt
```

### Configure project ###
```bash
cp {{ project_name }}/__local_settings.py {{ project_name }}/local_settings.py
vi {{ project_name }}/local_settings.py
```

### Sync database ###
```bash
python manage.py migrate
```

## Running ##
```bash
python manage.py runserver 0.0.0.0:8000
```

Open browser to http://127.0.0.1:8000

