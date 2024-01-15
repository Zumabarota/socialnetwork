# restaurantProject
An API for a basic Twitter clone built with Django & Django REST framework, based on the [Build a Social Network With Django project](https://realpython.com/django-social-network-1/) from Real Python.

# Description
API documentation in **Dwitter API.yaml**, to be displayed wherever (such as https://editor.swagger.io/).

This project serves as an example API for a basic Twitter clone, with features such as:

* Creation and display of users and dweets.
* Following and unfollowing of other accounts.
* Able to get all users, a specified user, all dweets, a specified dweet, all dweets from a specified user, all users the specified user follows/is followed by, and all dweets from users followed by the current user. 


Login is required for some HTTP requests (create/update/delete dweets, follow/unfollow users, show dweets from followed users).  Either create an account vis /register/, or use:

Login: admin

Pass: admin
