Bootstraping
============

Here a quick exemple on how to use the ioc to initialize a project.

First, create a ``start.py`` file with the following code. 

.. code-block:: python

    import sys, logging, optparse

    import ioc

    def main():
        parser = optparse.OptionParser()
        parser.add_option("-e", "--env", dest="env", help="Define the environment", default='dev')
        parser.add_option("-d", "--debug", dest="debug", action="store_true", default=False)

        options, args = parser.parse_args()

        if options.debug:
            logging.basicConfig(level=logging.DEBUG)

        container = ioc.build([
            'config/services.yml',
            'config/parameters_%s.yml' % options.env,
        ])

        ## adapt this line depends on your need
        container.get('myservice').start()


    if __name__ == "__main__":
        main()

Now you can create a ``services.yml`` containing services definitions:

.. code-block:: yaml

    parameters:
        app_name: My App

    services:
        my.service:
            class: module.ClassName
            arg: [arg1, @my.second.service]
            kwargs: 
                api_key:  '%external.service.api_key%'
                app_name: '%app.name%'

        my.second.service:
            class: logging.getLogger
            arguments:
                - 'logger_name'

If you need to have different configurations, another files can be defined. The switch will be done by the ``start.py`` script with the ``env`` option.

.. code-block:: yaml

    # configuration parameters_prod.yml
    parameters:
        external.service.api_key: XXXXXX

    # configuration parameters_dev.yml
    parameters:
        external.service.api_key: YYYYYY

The project can be started by using::

    python start.py -e prod