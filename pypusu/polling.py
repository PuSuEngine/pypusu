import json
from .threaded import PuSuClient as ThreadedPuSuClient

try:
    # Py2
    from Queue import Queue, Empty
except ImportError:
    # Py3
    from queue import Queue, Empty

DEBUG = False


class PuSuClient(ThreadedPuSuClient):
    """
    PuSu Engine client using the ws4py builtin client. Variant where reading
    messages takes polling, in case you want to avoid your code being called
    from another thread. Just make sure you poll often enough or the queue
    will use up your RAM.

    .. code-block:: python
        from pypusy.polling import PuSuClient

        client = PuSuClient("ws://127.0.0.1:55000")

        def listener(msg):
            print(msg)

        client.subscribe("my-channel", listener)
        client.publish("some-channel", "data")

        # Will call any subscribers if there were messages to deliver
        client.poll()
    """

    def __init__(self, *args):
        super(PuSuClient, self).__init__(*args)
        self._incoming_messages = Queue()
        if DEBUG:
            self.debug = True

    def poll(self):
        """
        Check for any new messages for us
        """
        count = 0
        while True:
            try:
                item = self._incoming_messages.get_nowait()
                count += 1
                self._on_receive(item)
            except Empty:
                break
        if self.debug:
            print("<< {} messages delivered from queue".format(count))

    def _received_message(self, data):
        if self.debug:
            print("<- {}".format(data))

        msg = json.loads(str(data))
        # Only publish messages should be paused, the rest is required for
        # normal function
        if msg["type"] == PuSuClient.TYPE_PUBLISH:
            self._incoming_messages.put(msg)
        else:
            self._on_receive(msg)
