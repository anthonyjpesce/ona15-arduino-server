#ONA15bot
---------

![](https://cloud.githubusercontent.com/assets/479290/9926577/98c8699e-5ccb-11e5-8613-d0a84547e8a0.png)

[Robots](http://www.slate.com/blogs/future_tense/2014/03/17/quakebot_los_angeles_times_robot_journalist_writes_article_on_la_earthquake.html) and [sensor journalism](https://www.google.com/search?q=sensor+journalism) are often discussed by digital journalists, but it's rare to see a simple, practical example.

At ONA15 we're bringing together the two with, what we hope, can be a straightforward example for journalists who are curious about the intersection of electronics, programming and reporting. With under $100 in equipment you can build a simple audio sensor that transmits to a server, then processes and stores the data, and runs a simple statistical analysis that powers a twitter "robot."

This readme covers the installation and setup of the server component. For a walkthrough of the electronics portion, including equipment and code for the Arduino, [check out our wiki](https://github.com/anthonyjpesce/ona15-arduino-server/wiki).

Getting started
---------------

Requirements:

* Python
* PostgreSQL
* virtualenv
* Git

Create a virtualenv to store the codebase.

```bash
$ virtualenv ona15-arduino-server
```

Activate the virtualenv.

```bash
$ cd ona15-arduino-server
$ . bin/activate
```

Clone the git repository from GitHub.

```bash
$ git clone git@github.com:anthonyjpesce/ona15-arduino-server.git repo
```

Enter the project and install its dependencies.

```bash
$ cd repo
$ pip install -r requirements.txt
```

You'll need to make a Postgres database locally before you can connect your Django project to it.

```bash
$ createdb soundtracker
```

Make a copy of settings_dev.py and settings_private.py and configure them to connect to your new database.

```bash
$ cp project/settings_dev.template project/settings_dev.py
$ cp project/settings_private.template project/settings_private.py
$ vim project/settings_dev.py
```

Let Django create the database tables you need.

```bash
$ python manage.py syncdb
$ python manage.py migrate
```

Load in some test data, if you want.

```bash
$ python manage.py loadtestdata
```

Run the test server for the first time.

```bash
$ python manage.py runserver
```

Check out the page at [localhost:8000](http://localhost:8000)
