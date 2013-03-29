Installation
============


First, obtain Python_ and virtualenv_ if you do not already have them. Using a
virtual environment will make the installation easier, and will help to avoid
clutter in your system-wide libraries. You will also need Git_ in order to
clone the repository.

.. _Python: http://www.python.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _Git: http://git-scm.com/

Once you have these, create a virtual environment somewhere on your disk, then
activate it::

    virtualenv myproject
    cd myproject
    source bin/activate

Now you can install the related required packages::

    pip install ioc



