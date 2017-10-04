from datetime import datetime
import time
import os
import sys

import stomp


class MyListener(stomp.ConnectionListener):

    def on_error(self, headers, message):
        print("Received an error")
        print("%s" % message)

    def on_message(self, headers, message):
        print("Received a message:")
        print("%s" % message)
        conn.ack(headers['message-id'])

    def on_disconnected(self):
        print('disconnected')
        connect_and_subscribe(self.conn)


if __name__ == '__main__':
    IP = os.getenv('YAMQ_CLIENT_IP', '127.0.0.1')
    PORT = os.getenv('YAMQ_CLIENT_PORT', 8000)

    conn = stomp.Connection12([(IP, PORT)])
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(wait=True)

    times = int(sys.argv[1])
    identifer = sys.argv[2]
    for i in range(times):
        print("Message send at: {}".format(datetime.now()))
        message = "From: {} Message no: {}".format(identifer, i)
        conn.send('/queue/test', message)
        time.sleep(1)
    time.sleep(1)
    print("Sending disconnect frame")
    conn.disconnect()
    print("Disconnecting the program")
