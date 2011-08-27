
import time
import threading

import helpers.kronos as kronos


class Reader(threading.Thread):
    def __init__(self, queue, writer, periodic=True, interval=1):
        self.writer = writer
        self.periodic = periodic
        self.interval = interval
        self.queue = queue
        self.setup()
        self.schedule_tasks()
        threading.Thread.__init__(self)

    def reschedule_tasks(self):
        self.schedule_tasks()
        self.scheduler.start()

    def schedule_tasks(self):
        self.scheduler = kronos.ThreadedScheduler()
        if self.periodic:
            self.schedule_interval_task()
        else:
            self.schedule_single_task()

    def schedule_interval_task(self):
        self.scheduler.add_interval_task(self.process,
                                         "periodic task",
                                         0,
                                         self.interval,
                                         kronos.method.threaded,
                                         [],
                                         None)

    def schedule_single_task(self):
        self.scheduler.add_single_task(self.process,
                                       "single task",
                                       0,
                                       kronos.method.threaded,
                                       [],
                                       None)

    def __writer_callback(self):
        """Callback to writer for non periodic tasks"""
        if not self.writer.periodic:
            self.writer.process()

    def _store(self, msg):
        if self.queue.qsize() < self.queue.maxsize:
            self.queue.put(msg)
            self.__writer_callback()
        else:
            print "discarding message [%s], full queue" % msg

    def process(self):
        msg = self._read()
        if not msg and self.periodic:
            print "discarding message due to an error"

    def _read(self):
        try:
            return self.read()
        except Exception, e:
            print "Can't read"
            print e
            return False

    def store(self, msg):
        try:
            self._store(msg)
        except Exception, e:
            print "Can't store in queue"
            print e
            return False

    def setup(self):
        """Subclasses should implement."""
        pass

    def read(self):
        """Subclasses should implement."""
        pass

    def run(self):
        self.scheduler.start()
