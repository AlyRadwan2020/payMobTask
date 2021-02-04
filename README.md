# Paymob task

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/AlyRadwan2020/payMobTask.git
$ cd payMobTask
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py makemigrations
```
Then
```sh
(env)$ python manage.py migrate
```
Once `migrations` have been finished , you need to create SuperAdmin user :

```sh
(env)$ python manage.py createsuperuser
```
Now you can navigate to `http://127.0.0.1:8000/admin/` to login .

Navigate to `http://127.0.0.1:8000/admin/task/normaluser/`. and create normal users 

And navigate to `http://127.0.0.1:8000/admin/task/adminuser/`. and create admin users



