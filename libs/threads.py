from threading import Thread


class MultiThreads:

    threads = []

    def __init__(self, th_id=None):
        self.__th_id = th_id

    def add_thread(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def start_all(self):
        for t in self.threads:  # starting all threads
            t.start()
        for t in self.threads:  # joining all threads
            t.join()
        self.threads = []
