import zmq


class Socket:
    def __init__(self, context, endpoint):
        self.socket = context.socket(zmq.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe("")

    def receive_parcel(self):
        envelope = self.socket.recv_multipart()
