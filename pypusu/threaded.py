import json
from ws4py.client.threadedclient import WebSocketClient
from .base import _PuSuBaseClient
from .errors import PyPuSuConnectionError

# Auto-patch ws4py with wsaccel if that's available
try:
    import wsaccel

    wsaccel.patch_ws4py()
except ImportError:
    pass

DEBUG = False


class _ThreadedWebSocketPassthrough(WebSocketClient):
    """
    Simple passthrough class to get messages from the ws4py threadedclient.
    """

    def __init__(self, parent, url):
        super(_ThreadedWebSocketPassthrough, self).__init__(
            url,
            protocols=['http-only']
        )
        self.parent = parent

    def closed(self, code, reason=None):
        """
        Called when connection is closed

        :param int code: Error code
        :param str reason: Human readable message
        """

        self.parent._on_close(code, reason)

    def received_message(self, message):
        """
        Called when server sends us a message

        :param ws4py.TextMessage message: The message data
        """

        self.parent._received_message(message)


class PuSuClient(_PuSuBaseClient):
    """
    PuSu Engine client using the ws4py builtin client, not terribly impressive,
    but doesn't depend on anything else.

    .. code-block:: python
        from pypusy.threaded import PuSuClient

        client = PuSuClient("ws://127.0.0.1:55000")

        def listener(msg):
            # Gotcha: will be called in a different thread.
            print(msg)

        client.subscribe("my-channel", listener)

        # If you want to receive your own messages (which normally you don't)
        # you could sleep and wait for the subscription to go through.

        client.publish("some-channel", "data")
    """

    def __init__(self, *args):
        super(PuSuClient, self).__init__(*args)
        if DEBUG:
            self.debug = True

    def connect(self):
        """
        Connect to the WSPS server, starts the thread. Does not promise that
        connection is up immediately when this function returns.
        """

        if not self._client:
            self._client = _ThreadedWebSocketPassthrough(self, self.server)
        self._waiting_for = "hello"
        self._client.connect()
        self._wait()

    def close(self, code=1000, reason="", wait=True):
        """
        Disconnect from the server.

        :param int code: Error code
        :param str reason: Human readable message
        :param bool wait: If we should wait for the thread to stop
        """

        self._client.close(code, reason)

        if wait:
            self._client.run_forever()

    def _send(self, data):
        if self.debug:
            print("-> {}".format(data))
        try:
            self._client.send(data)
        except AttributeError:
            # ws4py throws AttributeErrors when the server disconnects ..
            raise PyPuSuConnectionError("Looks like we're disconnected")

    def _received_message(self, data):
        if self.debug:
            print("<- {}".format(data))
        self._on_receive(json.loads(str(data)))
