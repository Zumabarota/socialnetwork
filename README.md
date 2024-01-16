# socialnetwork
An API for a basic Twitter clone built with Django & Django REST framework, based on the [Build a Social Network With Django project](https://realpython.com/django-social-network-1/) from Real Python.

# Description
This project serves as an example API for a basic Twitter clone.  API documentation is in **Dwitter API.yaml**, which can be viewed as-is or displayed using tools such as https://editor.swagger.io/.

# Features

* Creation and display of users and dweets, with the ability to follow and unfollow other users.
* Users: get all, get a single user, create a new user, login or logout, get all users that follow or are followed by the current user, follow or unfollow a single user, get a single user's dweets, get all dweets from followed users.
* Dweets: get all, get a single dweet, create a new dweet, edit or delete dweets created by the current user.

# Usage

To run, install the dependencies with

    $ pip install -r requirements.txt

and run with

    $ python manage.py runserver

which defaults to running on

``localhost:8000``

Login is required for some HTTP requests (create/update/delete dweets, follow/unfollow users, show dweets from followed users).  Either create an account vis /register/, or use:

Login: admin

Pass: admin
