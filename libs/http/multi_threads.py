
from threading import Thread


class MultiThreads:

    threads = []

    def __init__(self):
        self.threads = []

    def add(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def start(self, callback: callable=None):
        for t in self.threads:  # starting all threads
            t.start()
        for t in self.threads:  # joining all threads
            t.join()
            callable(callback) and callback()
        self.threads = []
