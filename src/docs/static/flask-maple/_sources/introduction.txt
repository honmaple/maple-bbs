1 Introduction To Flask-Maple
-----------------------------

1.1 Installation
~~~~~~~~~~~~~~~~

To install Flask-Maple:

.. code-block:: python

    pip install flask-maple

Or alternatively, you can download the repository and install manually by doing:

.. code-block:: python

    git clone git@github.com:honmaple/flask-maple.git
    cd flask-maple
    python setup.py install

1.2 Bootstrap
~~~~~~~~~~~~~

It's very sample to use bootstrap

.. code-block:: python

    from flask_maple import Bootstrap
    maple = Boostrap(app)

or you can register it by

.. code-block:: python

    maple = Bootstrap()
    maple.init_app(app)

**Templates:**

.. code-block:: html

    {% extends 'maple/base.html' %}
    {% block main -%}
    <button class="btn btn-primary">submit</button>
    <span class="glyphicon glyphicon-search" aria-hidden="true"></span>
    {% endblock -%}

**Config:**

.. code-block:: python

    AUTHOR_NAME = "This will show you name at html footer"

1.3 Captcha
~~~~~~~~~~~

Please install **Pillow** before use captcha

.. code-block:: python

    pip install pillow

**Usage**:

.. code-block:: python

    from flask_maple import Captcha
    captcha = Captcha(app)

Then you can visit `http://127.0.0.1/captcha <http://127.0.0.1/captcha>`_

**Config**:

.. code-block:: python

    CAPTCHA_URL = "The captcha url,default 'captcha'"

1.4 Error
~~~~~~~~~

You don't register app.errorhandler if you use error extension

**Usage**:

.. code-block:: python

    from flask_maple import Error
    error = Error(app)

This extension provides some simple error view

.. code-block:: python

    404
    403
    500

1.5 Login
~~~~~~~~~

It's easy to use login

.. code-block:: python

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
        password = db.Column(db.String(120), unique=True)


        def __repr__(self):
            return '<User %r>' % self.username

        @staticmethod
        def set_password(password):
            pw_hash = generate_password_hash(password)
            return pw_hash

        def check_password(self, password):
            return check_password_hash(self.password, password)

**Usage**:

.. code-block:: python

    from flask_maple import Auth
    auth = Auth(app, db=db, mail=mail, user_model=User)

If you use flask-principal,please set use_principal = True

.. code-block:: python

    from flask_maple import Auth
    auth = Auth(app, db=db, mail=mail, user_model=User,use_principal = True)

then you can visit `http://127.0.0.1:5000/login <http://127.0.0.1:5000/login>`_
