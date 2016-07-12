import json
from Queue import Queue, Empty

DEBUG = False


class PuSuException(Exception):
    pass


class TimeoutExceeded(PuSuException):
    """
    Exception raised if the timeout was exceeded waiting for confirmation on
    authorize or subscribe.
    """
    pass


class Message(object):
    """
    A message sent via PuSu to subscribers of a channel.
    """

    def __init__(self, data=None):
        self.type = None
        self.channel = None
        self.content = None

        if data:
            for key in data:
                setattr(self, key, data[key])


class _PuSuBaseClient(object):
    """
    Shared functionality of all PuSu clients, defines the common API.
    """

    TYPE_HELLO = "hello"
    TYPE_AUTHORIZE = "authorize"
    TYPE_AUTHORIZATION_OK = "authorization_ok"
    TYPE_PUBLISH = "publish"
    TYPE_SUBSCRIBE = "subscribe"
    TYPE_SUBSCRIBE_OK = "subscribe_ok"

    def __init__(self, server=None, onclose=None):
        """
        :param server: Full URI of the destination PuSu server, e.g.
                       ws://localhost:52525/
        :param function onclose: Optional callback to run when connection is
                                 closed for any reason.
        """
        self.debug = DEBUG
        self.server = server
        self.onclose = onclose
        self.timeout = 5.0  # seconds

        self._wait_queue = Queue()
        self._waiting_for = False
        self._client = None
        self._subscriptions = {}

        if server:
            self.connect()

    def connect(self):
        raise NotImplementedError("{cls} does not implement connect()".format(
            cls=self.__class__.__name__
        ))

    def close(self):
        raise NotImplementedError("{cls} does not implement connect()".format(
            cls=self.__class__.__name__
        ))

    def _send(self, data):
        raise NotImplementedError(
            "{cls} does not implement _send_message()".format(
                cls=self.__class__.__name__
            ))

    def publish(self, channel, content):
        """
        Publish a message to a channel.

        :param str channel: Name of the channel to publish to
        :param str|int|float|dict|list content: Data to send
        """
        self._send(json.dumps({
            "type": self.TYPE_PUBLISH,
            "channel": channel,
            "content": content
        }))

    def subscribe(self, channel, callback):
        """
        Register a callback to messages from a channel.

        :param str channel: Name of the channel to subscribe to
        :param function callback: Function that processes messages from this
                                  channel
        """
        if channel not in self._subscriptions:
            self._waiting_for = self.TYPE_SUBSCRIBE_OK
            self._send(json.dumps({
                "type": self.TYPE_SUBSCRIBE,
                "channel": channel
            }))
            self._wait()
        self._subscriptions[channel] = callback

    def authorize(self, authorization):
        """
        Process your authorization.

        :param str authorization: The authorization to present to the server.
        """
        self._waiting_for = self.TYPE_AUTHORIZATION_OK
        self._send(json.dumps({
            "type": self.TYPE_AUTHORIZE,
            "authorization": authorization
        }))
        self._wait()

    def _wait(self):
        try:
            if self.debug:
                print("Waiting for {}".format(self._waiting_for))
            self._wait_queue.get(timeout=self.timeout)
            if self.debug:
                print("Got {}".format(self._waiting_for))
        except Empty:
            raise TimeoutExceeded()
        finally:
            self._waiting_for = None

    def _on_receive(self, msg):
        if msg["type"] == self._waiting_for:
            self._wait_queue.put(True)

        if msg["type"] == self.TYPE_PUBLISH:
            self._deliver_message(msg)

    def _on_close(self, code, reason=None):
        if self.onclose:
            self.onclose(code, reason)

    def _deliver_message(self, msg):
        if msg["channel"] in self._subscriptions:
            self._subscriptions[msg["channel"]](msg["content"])
