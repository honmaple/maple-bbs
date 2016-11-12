1 Auth
------

1.1 Custom model
~~~~~~~~~~~~~~~~

You custom model if you need more when register or confirm email

1.1.1 register_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

1.1.2 confirm_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyAuth(Auth):
        def confirm_models(self, user):
            user.is_confirmed = True
            user.confirmed_time = datetime.now()
            self.db.session.commit()

1.1.3 email_models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class MyAuth(Auth):
        def email_models(self):
            current_user.send_email_time = datetime.now()
            self.db.session.commit()

1.2 Custom form
~~~~~~~~~~~~~~~

You can add custom form when register Auth

.. code-block:: python

    Auth(app, db=db, mail=mail, user_model=User,
         login_form=loginform,
         register_form=registerform,
         forget_form=forgetpasswordform)

**template**

.. code-block:: python

    templates/auth/login.html
    templates/auth/register.html
    templates/auth/forget.html
