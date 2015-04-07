import sys


class ProgressBar(object):
    """ProgressBar class holds the options of the progress bar.

    :type start: int | float
    :param start: State from which start the progress. For example, if start
        is 5 and the end is 10, the progress of this state is 50%

    :type end: int | float
    :param end: State in which the progress has terminated.

    :type width: int
    :param width: Width of a progress bar in symbols.

    :type fill: str
    :param fill: String to use for "filled" used to represent the progress

    :type blank: str
    :param blank: String to use for "blanked" used to represent remaining space.

    :type format: str
    :param format: Format of a progress bar. Default is [%(fill)s>%(blank)s] %(progress)s%%

    :type prefix: str
    :param prefix: String prefix of a progress bar.

    :type postfix: str
    :param postfix: String postfix of a progress bar.

    :type stream: file
    :param stream: File like object which shoot be used for output.
    """

    def __init__(self, start=0, end=10, width=12, fill='=', blank='.', format='[%(fill)s>%(blank)s] %(progress)s%%',
                 prefix='', postfix='', stream=sys.stdout):
        super(ProgressBar, self).__init__()

        self.__value_current = start
        self.__value_target = end
        self.__value_current_pct = self.__value_current*100/float(self.__value_target)
        self.__bar_width = width
        self.__bar_fill = fill
        self.__bar_blank = blank
        self.__format = prefix+format+postfix
        self.__step = 100 / float(width)
        self.__stream = stream

    @property
    def value(self):
        return self.__value_current

    @value.setter
    def value(self, value):
        self.__value_current = value
        self.__update_value_pct()

    @property
    def value_pct(self):
        return self.__value_current_pct

    def __update_value_pct(self):
        self.__value_current_pct = round(self.__value_current*100/float(self.__value_target))
        if self.__value_current_pct > 100:
            self.__value_current_pct = 100

    @property
    def target(self):
        return self.__value_target

    def __add__(self, increment):
        self.__value_current += increment
        self.__update_value_pct()
        return self

    def __str__(self):
        progress = int(self.__value_current_pct / self.__step)
        return self.__format % {'fill': progress * self.__bar_fill,
                                'blank': (self.__bar_width - progress) * self.__bar_blank,
                                'progress': self.__value_current_pct}

    __repr__ = __str__

    def show(self):
        self.__stream.write('\r')
        self.__stream.write(repr(self))
        self.__stream.flush()

    def update(self, transmitted, size):
        self.value = transmitted
        self.show()
        if transmitted == size:
            print

    def finish(self):
        self.value = self.__value_target
        self.show()
        print

    def reset(self):
        """Resets the current progress to the start point"""
        self.__value_current = 0
        self.__update_value_pct()
