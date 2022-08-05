from biumsputils.print import print

# Logger used by some decorators
class Logger():
    '''
        A basic logging system, used by the debugger decorator:
            it uses a custom print function that allows indentation
    '''
    OFF = -1
    DEBUG = 2
    INFO  = 1

    def __init__(self):
        self.state = Logger.OFF

    def set_state_debug(self):
        self.state = Logger.DEBUG

    def set_state_info(self):
        self.state = Logger.INFO

    def set_state_off(self):
        self.state = Logger.OFF                 

    def debug(self, *args, **kwargs):
        if self.state >= Logger.DEBUG:
            print(*args, **kwargs)
    
    def info(self, *args, **kwargs):
        if self.state >= Logger.INFO:
            print(*args, **kwargs)

logger = Logger()
