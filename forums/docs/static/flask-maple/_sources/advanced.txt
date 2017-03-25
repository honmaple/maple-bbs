1 Advanced
----------

1.1 Bootstrap
~~~~~~~~~~~~~

You can add you .js file or .css file with flask-assets

.. code-block:: python

    maple = MapleBootstrap(css=('style/xxx.css',),js=('style/xxx.js',))
    maple.init_app(app)

or you can add js or css in **templates**

.. code-block:: html

    {% block style -%}
    {{super()}}
    You css file
    {% endblock -%}

    {% block script -%}
    {{super()}}
    You js file
    {% endblock -%}

other **block**

.. code-block:: html

    {% block title -%}
    {% endblock -%}

1.2 Error
~~~~~~~~~

You can custom you template for error

.. code-block:: html

    templates/templet/error_404.html
    templates/templet/error_403.html
    templates/templet/error_500.html

1.3 Auth
~~~~~~~~

**Auth** api

.. code-block:: python

    Auth(app=None, db=none, mail=none, user_model=none, use_principal=false,
            login_form=loginform, register_form=registerform, forget_form=forgetpasswordform):

**db**

.. code-block:: python

    db = SQLAlchemy(app)
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    maplec = MapleCaptcha(app)
    mapleb = MapleBootstrap(app)
    mail = Mail(app)
    babel = Babel(app)

**mail**

.. code-block:: python

    mail = Mail(app)

**user_model**

.. code-block:: python

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True)
        email = db.Column(db.String(120), unique=True)
        password = db.Column(db.String(120), unique=True)

        def __repr__(self):
            return '<User %r>' % self.name

        @staticmethod
        def set_password(password):
            pw_hash = generate_password_hash(password)
            return pw_hash

        def check_password(self, password):
            return check_password_hash(self.password, password)

**use_principal**
if you use flask-principal,then set *use_principal = True*

**form**
You can customize form

**Custom Model**

1.3.1 register_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from flask_maple import Auth
    class MyAuth(Auth):
        def register_models(self, form):
            user = self.User()
            user.username = form.username.data
            user.password = user.set_password(form.password.data)
            user.email = form.email.data
            self.db.session.add(user)
            self.db.session.commit()
            return user

1.3.2 confirm_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyAuth(Auth):
        def confirm_models(self, user):
            user.is_confirmed = True
            user.confirmed_time = datetime.now()
            user.roles = 'writer'
            self.db.session.commit()

1.3.3 email_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyAuth(Auth):
        def email_models(self):
            current_user.send_email_time = datetime.now()
            self.db.session.commit()
