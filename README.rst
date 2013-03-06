============================
Python bindings for UCG API.
============================

`UCG <http://www.generateuniquecontent.com/index.php>`_ is an online
service for spinning text (synonym substitution)
that creates unique version(s) of existing text.
This package provides a way to easily interact with
`UCG API <http://www.generateuniquecontent.com/api.php>`_.
Usage requires an API subscription,
`get it here <http://www.generateuniquecontent.com/signup.php>`_.

* `Source code @ GitHub <https://github.com/niteoweb/ucg>`_


Install within virtualenv
=========================

.. sourcecode:: bash

    $ virtualenv foo
    $ cd foo
    $ git clone https://github.com/niteoweb/ucg
    $ bin/pip install ucg/

    # running tests:
    $ bin/pip install unittest2 mock
    $ bin/python -m unittest discover -s ucg/src/ucg/tests


Buildout
========

.. sourcecode:: bash

    $ git clone https://github.com/niteoweb/ucg
    $ virtualenv --no-site-packages ./ucg/
    $ cd ucg
    $ bin/python bootstrap.py
    $ bin/buildout

    # running tests and check code for imperfections
    $ ./pre-commit-hook.sh


Usage
=====

.. sourcecode:: python

    >>> from ucg import UCG
    >>> u = UCG("your@email.xyz", "yourapikey")
    >>> u.login()
    >>> print u.unique_variation(u"Some test text whič is fü.")
    u"Some trial cookie whič is fü."
    >>> u.logout()
