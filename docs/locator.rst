Resource Locator
================

The resource locator is a set of classes to find ... resource. A resource is a file located on the filesystem. 

Basic Usage
-----------

.. code-block:: python

        import ioc.locator

        locator = ioc.locator.FileSystemLocator(['/path/to/templates', '/other/path'])

        file = locator.locate("myfile.yml")

        # file => is a local path to the file


