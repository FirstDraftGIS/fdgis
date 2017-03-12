import signal
from signal import alarm, SIGALRM, signal

class Timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise OSError(self.error_message)
    def __enter__(self):
        signal(SIGALRM, self.handle_timeout)
        alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        alarm(0)
