PuSu Engine client for Python
=============================

Client for using the PuSu Engine server from Python. Probably much
better suitable for sending than receiving, but both should work.

Threaded example
----------------

If you want immediate delivery and are ok with your callbacks getting
called from another thread, you can use the threaded client.

.. code:: python

   from pypusu.threaded import PuSuClient
   from time import sleep


   if __name__ == "__main__":
       c = PuSuClient("ws://127.0.0.1:55000")

       count = 0


       def listener(msg):
           global count
           count += 1


       c.authorize("foo")
       c.subscribe("channel.1", listener)
       c.publish("channel.1", {"foo": "bar"})

       sleep(30)

       print(count)

Polling example
---------------

If your callbacks getting called from another thread is an issue, you
can use the polling client. Internally it still uses threads, but it
will not deliver the messages to your callbacks until you call
``poll()``.

.. code:: python

   from pypusu.polling import PuSuClient
   from time import sleep


   if __name__ == "__main__":
       c = PuSuClient("ws://127.0.0.1:55000")

       count = 0

       def listener(msg):
           global count
           count += 1

       c.authorize("foo")
       c.subscribe("channel.1", listener)
       c.publish("channel.1", {"foo": "bar"})

       for i in range(0, 30):
           sleep(1)
           c.poll()

       print(count)

Dependencies
------------

Not quite sure how to deal with dependencies yet, so for now you’ll have
to install them separately.

Both threaded and polling client need the following in your
``requirements.txt``:

::

   ws4py==0.3.5
   wsaccel==0.6.2

Or you can try:

::

   pip install ws4py wsaccel

License
-------

Short version: MIT + New BSD.

Long version: Read the LICENSE.md -file.

Uploading to PyPi
-----------------

You can’t really do that without the appropriate username + password
information, but I’m saving this here because I’ll just forget.

::

   python setup.py sdist upload -r pypitest
   python setup.py sdist upload -r pypi
