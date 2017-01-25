1 Bootstrap
-----------

1.1 Add css or js file
~~~~~~~~~~~~~~~~~~~~~~

You can add you .js file or .css file with flask-assets

.. code-block:: python

    maple = Bootstrap(css=('style/xxx.css',),js=('style/xxx.js',))
    maple.init_app(app)

Or you can add js or css in **templates**

.. code-block:: html

    {% block style -%}
    {{super()}}
    You css file
    {% endblock -%}
    {% block script -%}
    {{super()}}
    You js file
    {% endblock -%}

1.2 use auth extension
~~~~~~~~~~~~~~~~~~~~~~

If you want use maple auth extension,you need set

.. code-block:: python

    Bootstrap(app,use_auth=True)

But before it,you need register csrf,beacuse ajax need csrf.

.. code-block:: python

    from flask_wtf.csrf import CsrfProtect
    csrf = CsrfProtect()
    csrf.init_app(app)

1.3 Other block
~~~~~~~~~~~~~~~

.. code-block:: html

    {% block title -%}
    {% endblock -%}

1.4 Custom footer
~~~~~~~~~~~~~~~~~

The footer file in **templates/maple/footer.html**,you can custom it.

.. code-block:: html

    <div class="footer text-center">
    custom content
    </div>
