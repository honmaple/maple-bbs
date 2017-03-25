.. Flask-Avatar documentation master file, created by
   sphinx-quickstart on Sat Jul  2 20:55:02 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-Avatar's documentation!
========================================

It's easy to generate avatar for flask.


1.1 Installation
~~~~~~~~~~~~~~~~

To install Flask-Avatar:

.. code-block:: shell

    pip install flask-avatar

Or alternatively, you can download the repository and install manually by doing:

.. code-block:: sehll

    git clone git@github.com:honmaple/flask-avatar.git
    cd flask-avatar
    python setup.py install

1.2 Usage
~~~~~~~~~

.. code-block:: python

    from flask_avatar import Avatar
    [...]
    Avatar(app)

Templates:

.. code-block:: html

    {{ url_for('avatar',text = user.username )}}

1.3 Config
~~~~~~~~~~

AVATAR_URL = "The avatar url,default 'avatar'"

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

