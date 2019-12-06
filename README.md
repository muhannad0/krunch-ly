# KrunchLy URL Shortener
A small Python Flask application to generate short links

### Features
- Generate short link
- Redirect to original link
- Show all generated links

## Running with Docker
```
docker build -t krunchly:latest .
docker run -d -p 8000:5000 --rm krunchly:latest
```

## Installation on a Linux Machine
These installation steps were done on Ubuntu 18.04 LTS. YMMV on other OS, but the general idea is the same. Basically you need a Python 3 environment, a webserver (I'm using gunicorn and nginx here) and a MySQL database.

### Install required packages
```
sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-dev python3-pip
sudo apt-get -y install mysql-server supervisor nginx git
```
### Setup the app
```
git clone https://github.com/muhannad0/krunch-ly.git
cd krunch-ly
python3 -m venv venv
source venv/bin/activate
(venv) pip3 install -r requirements.txt
(venv) pip3 install gunicorn pymysql
```

### Create the environment variables
Create .env file in base directory with variables below
```
SECRET_KEY=super-secret-key
DATABASE_URL=mysql+pymysql://<db_user>:<db_password>@localhost:3306/<db_name>
```

Export variable for entry point to Flask application
```
echo "export FLASK_APP=krunchly.py" >> ~/.profile
```

### Prepare the database
Login as with root user and create database and user. Remember to update .env file with the correct info used here.
```
CREATE DATABASE <db_name>;
CREATE USER '<db_user>'@'localhost' IDENTIFIED BY '<db_password>';
GRANT ALL PRIVILEGES ON <db_name>.* to '<db_user>'@'localhost';
FLUSH PRIVILEGES;
QUIT;
```

Populate the database.
```
(venv) flask db upgrade
```

### Run app using Gunicorn with Supervisor
Create a supervisor config to run the app using Gunicorn. Below is a sample configuration.

sudo vi /etc/supervisor/conf.d/krunchly.conf
```
[program:krunchly]
command=/home/ubuntu/krunch-ly/venv/bin/gunicorn -b localhost:8000 -w 4 krunchly:app
directory=/home/ubuntu/krunch-ly
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```
Reload supervisor service for new config to be loaded
```
sudo supervisorctl reload
```

### Setup nginx
We will be deploying it as the only HTTP site on the server. To start we'll remove the default config.
```
sudo rm /etc/nginx/sites-enabled/default
```
Create a new virtualhost for our application.

sudo vi /etc/nginx/sites-available/krunchly
```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    access_log /var/log/nginx/krunchly_access.log;
    error_log /var/log/nginx/krunchly_error.log;
}
```
Create a symlink to enable the virtualhost.
```
sudo ln -s /etc/nginx/sites-available/krunchly /etc/nginx/sites-enabled/krunchly
```

Reload nginx service.
```
sudo systemctl reload nginx
```

You should now be able to access the app from the browser.

## Author
Mohamed Muhannad ([@monde_](https://twitter.com/monde_))

## Acknowledgements
- [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg