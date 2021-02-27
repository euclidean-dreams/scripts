class Signaler:
    def __init__(self):
        self.shutdown = False

    def should_shutdown(self):
        return self.shutdown

    def signal_shutdown(self):
        self.shutdown = True
