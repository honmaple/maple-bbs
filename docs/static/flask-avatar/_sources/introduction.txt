1 flask-avatar
--------------

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
