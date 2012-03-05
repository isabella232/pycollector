import logging
from third import filetail

from __reader import Reader
from __message import Message


class LogReader(Reader):
    """Conf:
        - logpath (required): path of log file,
            e.g. /tmp/my.log
        - delimiter (optional): character to split log lines,
            e.g. '\t'
        - columns (optional): list of columns for each log line,
            e.g. ['date', 'hour', 'message']"""

    def setup(self):
        self.log = logging.getLogger()
        self.tail = filetail.Tail(self.logpath, max_sleep=1)
        self.checkpoint = 0

    def process_line(self):
        try:
            line = self.tail.nextline()
            to_store = line

            if hasattr(self, 'delimiter'):
                to_store = to_store.strip().split(self.delimiter)

                if hasattr(self, 'columns'):
                    to_store = dict(zip(self.columns, to_store))

            if self.store(Message(content=to_store,
                               checkpoint=self.checkpoint)):
                self.checkpoint += 1

            return True
        except Exception, e:
            self.log.error('error reading line, maybe it was rotated')
            return False
    
    def read(self):
        if self.period:
            return self.process_line()
        else:            
            while True:
                self.process_line()
