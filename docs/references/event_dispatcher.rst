Event Dispatcher
================

The ioc package provides an optional Event Dispatcher. The dispatcher is always set if you use the ``ioc.build`` function.

Basic Usage
-----------

.. code-block:: python

    import ioc.event

    def mylistener(event):
        event.get('node')['value'] = event.get('node')['value'] * 60
        event.stop_propagation()

    dispatcher = ioc.event.Dispatcher()
    dispatcher.add_listener('event.name', mylistener)

    event = dispatcher.dispatch('event.name', {
        'node': { 'value': 2 }
    })

    