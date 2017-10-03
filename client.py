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


if __name__ == '__main__':
    IP = os.getenv('YAMQ_CLIENT_IP', '127.0.0.1')
    PORT = os.getenv('YAMQ_CLIENT_PORT', 8000)

    conn = stomp.Connection12([(IP, PORT)])
    conn.set_listener('', MyListener())
    conn.start()
    conn.connect(wait=True)

    conn.subscribe(destination='/queue/test', id=1, ack='client')

    continue_loop = True
    print("Press 'c' to terminate the program")
    while continue_loop:
        command = input('')
        if command == 'c':
            continue_loop = False
    conn.disconnect()
