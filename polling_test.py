from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div
from pypusu.polling import PuSuClient
from time import sleep, time

if __name__ == "__main__":
    print("Connecting")
    c = PuSuClient("ws://127.0.0.1:55000")

    count = 0

    def listener(msg):
        global count
        count += 1

    print("Authorizing")
    c.authorize("foo")
    print("Subscribing")
    c.subscribe("channel.1", listener)

    print("Waiting")

    target = 500
    start = time()
    for i in range(1, target + 1):
        c.publish("channel.1", {"foo": "bar"})
    end = time()
    elapsed = end - start

    print("Sent {} messages in {:.3f}s, {:.2f}msg/s".format(
        target,
        elapsed,
        old_div(target, elapsed)
    ))

    sleep(1)
    print("So far got {} messages, polling...".format(count))
    c.poll()
    print("After poll got {} messages, waiting for more...".format(count))

    for i in range(0, 60):
        sleep(1)
        c.poll()

    print("Got {} messages".format(count))
